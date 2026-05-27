# 🎙️ AI Voice Replacement System
## Automatic Multilingual Video Dubbing using Generative AI

A full-stack Generative AI application that automates multilingual video dubbing through speech recognition, translation, AI voice synthesis, and audio-video synchronization.

The system enables users to upload a video, transcribe spoken content, translate it into supported languages, generate natural AI speech, and produce a dubbed output video through an end-to-end automated pipeline.

---

## 🚀 Features

- Upload and process video files through a web interface
- Speech-to-text transcription using Faster-Whisper
- Multilingual translation support
- AI-powered voice generation using ElevenLabs
- Automatic synchronization of generated audio with video
- Video rendering and export using FFmpeg
- Responsive Glassmorphism-based UI

---

## 🧠 System Workflow

Upload Video  
↓  
Extract Audio  
↓  
Speech Recognition (Whisper)  
↓  
Language Translation  
↓  
AI Voice Synthesis  
↓  
Audio–Video Synchronization  
↓  
Generate Final Dubbed Video  

---

## 🛠 Tech Stack

| Layer | Technologies |
|--------|-------------|
| Frontend | HTML, CSS, Bootstrap |
| Backend | Flask, Python |
| Speech Recognition | Faster-Whisper |
| Translation | Googletrans |
| Voice Generation | ElevenLabs API |
| Video Processing | MoviePy, FFmpeg |
| Environment | Python 3.10+ |

---

## 📊 Project Metrics

| Metric | Value |
|---------|-------|
| Supported Languages | 3 |
| Processing Pipeline | Fully Automated |
| Architecture | End-to-End GenAI |
| Deployment Type | Local Web Application |
| Processing Mode | Video → Audio → AI Voice → Video |

---

## 📂 Project Structure

```bash
AI-Voice-Replacement-System/
│
├── static/
├── templates/
├── uploads/
├── output/
├── app.py
├── requirements.txt
├── api.env
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/Yash-Ghyar/AI-Voice-Replacement-System.git
cd AI-Voice-Replacement-System
```

### Create Virtual Environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install Dependencies:

```bash
pip install -r requirements.txt
```

Run Application:

```bash
python app.py
```

Open:

```bash
http://127.0.0.1:5000
```

---

## 🔐 Environment Variables

Create an `api.env` file:

```env
ELEVEN_API_KEY=your_api_key
ELEVEN_VOICE_ID=default_voice_id
VOICE_ID_EN=english_voice_id
VOICE_ID_HI=hindi_voice_id
VOICE_ID_MR=marathi_voice_id
```

---

## 🎯 Future Improvements

- Additional language support
- Real-time dubbing
- Lip-sync enhancement
- Cloud deployment
- User authentication

---

## 👨‍💻 Author

**Yash Ghyar**  
B.Tech – Artificial Intelligence & Data Science  
VIT Pune

---
⭐ If you found this project useful, consider giving it a star.
