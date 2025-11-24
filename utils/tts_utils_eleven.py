import os
import requests

def generate_ai_voice(text):
    print("🎤 Generating AI voice via ElevenLabs...")

    api_key = os.getenv("ELEVEN_API_KEY") or "YOUR_API_KEY_HERE"
    voice_id = "pNInz6obpgDQGcFmaJgB"  # default voice, change if needed

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "voice_settings": {"stability": 0.6, "similarity_boost": 0.85}
    }

    response = requests.post(url, headers=headers, json=payload)
    ai_audio_path = os.path.join("assets/outputs", "ai_audio.wav")

    with open(ai_audio_path, "wb") as f:
        f.write(response.content)

    print("✅ Voice saved:", ai_audio_path)
    return ai_audio_path
