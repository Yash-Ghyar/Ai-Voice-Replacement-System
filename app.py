import os
import uuid
import traceback
from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from dotenv import load_dotenv
import requests
from moviepy.editor import VideoFileClip, AudioFileClip
from werkzeug.utils import secure_filename
from faster_whisper import WhisperModel
import torch

# translation (optional)
try:
    from googletrans import Translator
    translator = Translator()
    HAVE_TRANSLATOR = True
except:
    translator = None
    HAVE_TRANSLATOR = False


app = Flask(__name__, static_folder="static", template_folder="templates")
app.config["MAX_CONTENT_LENGTH"] = 500 * 1024 * 1024   # 500 MB upload limit

load_dotenv("api.env")

BASE = os.getcwd()
UPLOAD_FOLDER = os.path.join(BASE, "uploads")
OUTPUT_FOLDER = os.path.join(BASE, "assets", "outputs")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
VOICE_ID = os.getenv("ELEVEN_VOICE_ID")

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
whisper_model = WhisperModel("small", device=DEVICE)
print("Whisper Loaded!", DEVICE)


# -------------------------
# Helper functions
# -------------------------
def safe_filename(original):
    base = secure_filename(original)
    return f"{uuid.uuid4().hex[:8]}_{base}"


def extract_audio(video, wav_out):
    clip = VideoFileClip(video)
    clip.audio.write_audiofile(wav_out, codec="pcm_s16le", verbose=False, logger=None)
    clip.close()


def transcribe_audio(wav):
    segments, _ = whisper_model.transcribe(wav)
    return " ".join([s.text.strip() for s in segments])


def translate_text(text, lang):
    if not HAVE_TRANSLATOR:
        return text
    try:
        if lang == "hindi":
            return translator.translate(text, dest="hi").text
        return translator.translate(text, dest="en").text
    except:
        return text


def ai_voice(text, out):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream"
    headers = {"xi-api-key": ELEVEN_API_KEY}
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.8}
    }
    r = requests.post(url, json=payload, headers=headers, stream=True)
    with open(out, "wb") as f:
        for chunk in r.iter_content(4096):
            f.write(chunk)


def merge_audio(video, audio, out):
    v = VideoFileClip(video)
    a = AudioFileClip(audio)

    if a.duration > v.duration:
        a = a.subclip(0, v.duration)

    final = v.set_audio(a)
    final.write_videofile(out, codec="libx264", audio_codec="aac",
                          verbose=False, logger=None)
    v.close()
    a.close()
    final.close()


# -------------------------
# Routes
# -------------------------

@app.route("/")
def index():
    return render_template("index.html")


# ⭐ FIX ROUTE: Add GET for browser prefetch
@app.route("/start", methods=["GET"])
def start_redirect():
    return redirect("/")


# Step 1 → Upload file, go to spinner page
@app.route("/start", methods=["POST"])
def start():
    try:
        vid = request.files.get("video")
        lang = request.form.get("target_lang")

        if not vid:
            return "No file uploaded", 400

        saved_name = safe_filename(vid.filename)
        saved_path = os.path.join(UPLOAD_FOLDER, saved_name)
        vid.save(saved_path)

        return render_template("processing.html",
                               filename=saved_name,
                               lang=lang)

    except Exception as e:
        traceback.print_exc()
        return f"Error: {str(e)}", 500


# Step 2 → Heavy processing (triggered automatically by spinner)
@app.route("/process_real")
def process_real():
    try:
        filename = request.args.get("filename")
        lang = request.args.get("lang")

        uid = uuid.uuid4().hex[:8]
        src_wav = os.path.join(UPLOAD_FOLDER, f"{uid}_src.wav")
        ai_wav = os.path.join(OUTPUT_FOLDER, f"{uid}_ai.wav")
        final_vid = os.path.join(OUTPUT_FOLDER, f"{uid}_final.mp4")

        video_path = os.path.join(UPLOAD_FOLDER, filename)

        extract_audio(video_path, src_wav)
        text = transcribe_audio(src_wav)
        translated = translate_text(text, lang)
        ai_voice(translated, ai_wav)
        merge_audio(video_path, ai_wav, final_vid)

        return render_template("result.html",
                               output_video=os.path.basename(final_vid))

    except Exception as e:
        traceback.print_exc()
        return "Processing failed: " + str(e)


@app.route("/assets/outputs/<path:filename>")
def serve_video(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)


if __name__ == "__main__":
    app.run(debug=True)
