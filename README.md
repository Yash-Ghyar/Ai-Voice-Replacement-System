🎙️ AI Voice Replacement System

An advanced AI-powered voice transformation system that replaces the voice in any short video (≤20 seconds) using Speech Recognition, Text-to-Speech (TTS), and Audio-Video Syncing technologies — all built using Flask and cutting-edge AI models.

🚀 Overview

The AI Voice Replacement System allows users to upload a short video, extract and transcribe its speech using Whisper AI, generate a new voice using TTS models like Bark, ElevenLabs, or OpenVoice, and finally merge the new audio with the original video seamlessly.

It’s a complete end-to-end GenAI + Flask application, showcasing your full-stack AI engineering capability.

🧠 Tech Stack

Frontend:

HTML5, CSS3, Bootstrap 5

Animated UI with glassmorphism and glowing effects

Backend:

Flask (Python)

OpenAI Whisper (Speech-to-Text)

Bark / ElevenLabs / OpenVoice (TTS Engines)

MoviePy & FFmpeg (Video Editing)

Environment:

Python 3.10+

Render Deployment Ready (Production Environment)

✨ Features

🎧 Extracts and transcribes voice from any short video

🧩 Detects language automatically (English / Hindi)

🗣️ Replaces voice using multiple AI TTS engines

🎬 Merges generated audio back into the original video

💻 Modern, cinematic, and responsive frontend (Bootstrap + Glow UI)

🚀 Fully functional Flask backend (ready for deployment)

⚙️ Installation
# Clone the repository
git clone https://github.com/Yash-Ghyar/Ai-Voice-Replacement-System.git
cd Ai-Voice-Replacement-System

# Create a virtual environment
python -m venv venv
venv\Scripts\activate  # for Windows

# Install dependencies
pip install -r requirements.txt

▶️ Run the Application
python app.py


Then open your browser and go to:

http://127.0.0.1:5000

🧩 Workflow

Upload Video: User uploads a short video (≤20 seconds).

Transcription: Audio is extracted and transcribed using Whisper AI.

Voice Replacement: A new voice is generated using AI TTS models.

Video Reconstruction: The generated voice replaces the original one.

Result Page: The processed video is displayed with download option.

🛠️ Model Info

Speech Recognition: OpenAI Whisper (base model)

Text-to-Speech Options:

Bark – Local small model (fast & free)

ElevenLabs API – Realistic human voices

OpenVoice – Cross-lingual cloning