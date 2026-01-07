import os
import uuid
import traceback
from flask import Flask, render_template, request, send_from_directory, redirect
from dotenv import load_dotenv
import requests
from moviepy.editor import VideoFileClip, AudioFileClip
from werkzeug.utils import secure_filename
from faster_whisper import WhisperModel
import torch

# Optional translation
try:
    from googletrans import Translator
    translator = Translator()
    HAVE_TRANSLATOR = True
except Exception:
    translator = None
    HAVE_TRANSLATOR = False

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config["MAX_CONTENT_LENGTH"] = 500 * 1024 * 1024  # 500MB

# Load API keys
load_dotenv("api.env")

BASE = os.getcwd()
UPLOAD_FOLDER = os.path.join(BASE, "uploads")
OUTPUT_FOLDER = os.path.join(BASE, "assets", "outputs")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")

# Default voice (fallback if specific ones are missing)
VOICE_ID_DEFAULT = os.getenv("ELEVEN_VOICE_ID")

# Optional specific voices for each reference file (if you set them in api.env)
VOICE_ID_EN = os.getenv("VOICE_ID_EN")   # for ref_voice_en.wav
VOICE_ID_HI = os.getenv("VOICE_ID_HI")   # for ref_voice_hi.wav
VOICE_ID_MR = os.getenv("VOICE_ID_MR")   # for ref_voice_mr.wav

# Map reference voice filenames to ElevenLabs voice IDs
VOICE_MAP = {
    "voices/ref_voice_en.wav": VOICE_ID_EN or VOICE_ID_DEFAULT,
    "voices/ref_voice_hi.wav": VOICE_ID_HI or VOICE_ID_DEFAULT,
    "voices/ref_voice_mr.wav": VOICE_ID_MR or VOICE_ID_DEFAULT,
}

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
whisper_model = WhisperModel("small", device=DEVICE)
print("Whisper Loaded!", DEVICE)

# ------------------------------------
# Utils
# ------------------------------------


def safe_filename(original: str) -> str:
    base = secure_filename(original)
    return f"{uuid.uuid4().hex[:8]}_{base}"


def extract_audio(video: str, wav_out: str) -> None:
    clip = VideoFileClip(video)
    clip.audio.write_audiofile(
        wav_out, codec="pcm_s16le", verbose=False, logger=None
    )
    clip.close()


def transcribe_audio(wav: str) -> str:
    segments, _ = whisper_model.transcribe(wav)
    return " ".join([s.text.strip() for s in segments])


def translate_text(text: str, lang: str) -> str:
    """Translate text based on selected target language."""
    if not HAVE_TRANSLATOR:
        return text

    try:
        if lang == "hindi":
            return translator.translate(text, dest="hi").text
        elif lang == "marathi":
            return translator.translate(text, dest="mr").text
        else:
            # default: english
            return translator.translate(text, dest="en").text
    except Exception:
        return text


# ------------------------------------
# AI VOICE FUNCTION (USES REFERENCE VOICE)
# ------------------------------------


def ai_voice(text: str, out: str, ref_voice: str | None) -> str | None:
    print("\n********** ENTERED ai_voice() ***********\n")
    print("TEXT RECEIVED:", text)

    # Decide which ElevenLabs voice to use
    selected_voice_id = VOICE_MAP.get(ref_voice, VOICE_ID_DEFAULT)

    if not selected_voice_id:
        print("No valid VOICE_ID found. Check your api.env.")
        return None

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{selected_voice_id}/stream"
    headers = {"xi-api-key": ELEVEN_API_KEY}
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.8},
    }

    try:
        r = requests.post(url, json=payload, headers=headers, stream=True)
    except Exception as e:
        print("REQUEST FAILED:", str(e))
        return None

    print("\n================ ELEVENLABS DEBUG ================")
    print("STATUS CODE:", r.status_code)
    print("HEADERS:", r.headers)
    print("RAW RESPONSE (first 500 bytes):", r.content[:500])
    print("===================================================\n")

    with open(out, "wb") as f:
        f.write(r.content)

    print("FILE SAVED:", out, "| SIZE:", os.path.getsize(out), "bytes")

    return out


# ------------------------------------
# Merge video + audio
# ------------------------------------


def merge_audio(video: str, audio: str, out: str) -> None:
    v = VideoFileClip(video)
    a = AudioFileClip(audio)

    if a.duration > v.duration:
        a = a.subclip(0, v.duration)

    final = v.set_audio(a)
    final.write_videofile(
        out,
        codec="libx264",
        audio_codec="aac",
        verbose=False,
        logger=None,
    )

    v.close()
    a.close()
    final.close()


# ------------------------------------
# Routes
# ------------------------------------


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/start", methods=["GET"])
def start_redirect():
    return redirect("/")


@app.route("/start", methods=["POST"])
def start():
    try:
        vid = request.files.get("video")
        lang = request.form.get("target_lang")
        ref_voice = request.form.get("ref_voice")  # NEW: which reference voice

        if not vid:
            return "No file uploaded", 400

        saved_name = safe_filename(vid.filename)
        saved_path = os.path.join(UPLOAD_FOLDER, saved_name)
        vid.save(saved_path)

        # Pass ref_voice through to processing page
        return render_template(
            "processing.html",
            filename=saved_name,
            lang=lang,
            ref_voice=ref_voice,
        )

    except Exception as e:
        traceback.print_exc()
        return "Error: " + str(e), 500


@app.route("/process_real")
def process_real():
    try:
        filename = request.args.get("filename")
        lang = request.args.get("lang")
        ref_voice = request.args.get("ref_voice")  # NEW

        uid = uuid.uuid4().hex[:8]
        src_wav = os.path.join(UPLOAD_FOLDER, f"{uid}_src.wav")
        ai_wav = os.path.join(OUTPUT_FOLDER, f"{uid}_ai.wav")
        final_vid = os.path.join(OUTPUT_FOLDER, f"{uid}_final.mp4")

        video_path = os.path.join(UPLOAD_FOLDER, filename)

        extract_audio(video_path, src_wav)
        text = transcribe_audio(src_wav)
        translated = translate_text(text, lang)
        ai_voice(translated, ai_wav, ref_voice)
        merge_audio(video_path, ai_wav, final_vid)

        return render_template(
            "result.html", output_video=os.path.basename(final_vid)
        )

    except Exception as e:
        traceback.print_exc()
        return "Processing failed: " + str(e)


@app.route("/assets/outputs/<path:filename>")
def serve_video(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)


if __name__ == "__main__":
    app.run(debug=False)
