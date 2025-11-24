import os
from flask import Flask, render_template, request, send_from_directory
from dotenv import load_dotenv
import requests
from moviepy.editor import VideoFileClip, AudioFileClip
from werkzeug.utils import secure_filename
from faster_whisper import WhisperModel
import torch

# ------------------ CONFIG ------------------
app = Flask(__name__)
load_dotenv("api.env")

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "assets/outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
VOICE_ID = os.getenv("ELEVEN_VOICE_ID")

# Load Whisper ONCE (important!!)
WHISPER_DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
whisper_model = WhisperModel("small", device=WHISPER_DEVICE)
print("🔥 Whisper model loaded ONCE!")


# ------------------ STEP 1: Extract audio ------------------
def extract_audio(video_path, output_audio_path):
    print("🎬 Extracting audio...")
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(output_audio_path, verbose=False, logger=None)
    clip.close()
    print("✅ Audio extracted:", output_audio_path)


# ------------------ STEP 2: Transcribe ------------------
def transcribe_audio(audio_path):
    print(f"🎧 Transcribing: {audio_path}")
    segments, _ = whisper_model.transcribe(audio_path)

    text = " ".join([seg.text.strip() for seg in segments])
    print("📝 Transcribed text preview:", text[:150], "...")
    return text


# ------------------ STEP 3: Generate AI Voice (ElevenLabs) ------------------
def generate_ai_voice(text, output_path):
    print("🎤 Generating AI voice via ElevenLabs...")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream"

    headers = {"xi-api-key": ELEVEN_API_KEY}

    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.8},
    }

    response = requests.post(url, json=data, headers=headers, stream=True)

    if response.status_code != 200:
        raise Exception(
            f"❌ ElevenLabs Error: {response.status_code} {response.text}"
        )

    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=4096):
            f.write(chunk)

    print("✅ AI voice saved:", output_path)


# ------------------ STEP 4: Replace Audio in Video ------------------
def replace_audio_in_video(video_path, new_audio_path, output_video_path):
    print("🎥 Combining video with AI audio...")

    video = VideoFileClip(video_path)
    new_audio = AudioFileClip(new_audio_path)

    if new_audio.duration > video.duration:
        new_audio = new_audio.subclip(0, video.duration)

    final = video.set_audio(new_audio)
    final.write_videofile(
        output_video_path,
        codec="libx264",
        audio_codec="aac",
        verbose=False,
        logger=None,
    )

    video.close()
    new_audio.close()
    final.close()

    print("✅ Final video saved:", output_video_path)


# ------------------ ROUTES ------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload_video", methods=["POST"])
def upload_video():
    file = request.files.get("video")
    if not file:
        return "❌ No video uploaded"

    # Safe filename
    filename = secure_filename(file.filename)
    video_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(video_path)

    extracted_audio = os.path.join(UPLOAD_FOLDER, "extracted.wav")
    ai_audio = os.path.join(OUTPUT_FOLDER, "ai_voice.wav")
    final_video = os.path.join(OUTPUT_FOLDER, "final_output.mp4")

    # Pipeline
    extract_audio(video_path, extracted_audio)
    text = transcribe_audio(extracted_audio)
    generate_ai_voice(text, ai_audio)
    replace_audio_in_video(video_path, ai_audio, final_video)

    return render_template(
        "result.html", output_video="final_output.mp4"
    )


@app.route("/assets/outputs/<path:filename>")
def serve_video(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)


# ------------------ MAIN ------------------
if __name__ == "__main__":
    app.run(debug=True)
