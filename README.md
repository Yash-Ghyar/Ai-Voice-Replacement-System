🎙️ AI Voice Replacement System

Automatic Multilingual Video Dubbing using GenAI

A full-stack GenAI web application that enables automatic voice replacement in videos.
Users can upload a video, transcribe its audio using Whisper, translate it into English, Hindi, or Marathi, generate a new AI voice using ElevenLabs, and merge the synthesized audio back into the original video — all through a Flask-based web interface.

🚀 Key Features

Upload short videos for processing

High-accuracy speech-to-text using Faster-Whisper

Multilingual translation (English / Hindi / Marathi)

AI voice synthesis using ElevenLabs

Automatic audio–video synchronization and merging

Modern Glassmorphism UI with animated background

🧠 Tech Stack

Frontend: HTML, CSS, Bootstrap
Backend: Flask, Faster-Whisper, Googletrans, ElevenLabs API
Video Processing: MoviePy, FFmpeg
Environment: Python 3.10+

🔧 Installation
git clone https://github.com/Yash-Ghyar/AI-Voice-Replacement-System.git
cd AI-Voice-Replacement-System

python -m venv venv
venv\Scripts\activate   # Windows

pip install -r requirements.txt
python app.py


Open in browser:
👉 http://127.0.0.1:5000

🔐 Environment Variables (api.env)
ELEVEN_API_KEY=your_api_key
ELEVEN_VOICE_ID=default_voice_id
VOICE_ID_EN=english_voice_id
VOICE_ID_HI=hindi_voice_id
VOICE_ID_MR=marathi_voice_id