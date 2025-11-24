import whisper

def transcribe_audio(audio_path):
    print("🎧 Transcribing:", audio_path)
    model = whisper.load_model("base")  # use "small" or "medium" for better accuracy
    result = model.transcribe(audio_path)
    text = result['text']
    print("✅ Transcription done!")
    print("📝 Text (preview):", text[:100], "...")
    return text
