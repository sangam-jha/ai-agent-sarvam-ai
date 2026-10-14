<div align="center">

# 🎙️ Sarvam Voice Studio

**Create, summarize, and translate speech across 23 Indian languages — powered by [Sarvam AI](https://www.sarvam.ai/).**

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Sarvam AI](https://img.shields.io/badge/Powered%20by-Sarvam%20AI-orange)
![License](https://img.shields.io/badge/License-MIT-green)

</div>

---

## ✨ Overview

**Sarvam Voice Studio** is a Streamlit web app that turns text, documents, and audio into natural-sounding speech in Indian languages. It chains together several Sarvam AI models (speech-to-text, translation, document OCR, LLM summarization, and text-to-speech) into three simple workflows.

## 🚀 Features

| Workflow | What it does |
|---|---|
| **Text to speech** | Type or paste text (up to 2,500 chars) or upload a PDF/image, optionally translate it, and generate speech. |
| **Summarize & speak** | Summarize long text (up to 100,000 chars) or a document into a short English summary, translate it, and read it aloud. |
| **Translate speech** | Upload an audio file, transcribe it, translate it into another language, and get spoken audio back. |

**Highlights**

- 🌐 **23 input languages** including Hindi, Bengali, Tamil, Telugu, Kannada, Malayalam, Marathi, Gujarati, Punjabi, Odia, Assamese, Urdu, Nepali, Sanskrit, Kashmiri, Santali, and more
- 🔊 **11 output (TTS) languages** with **37 voices** (23 male, 14 female)
- 📄 **Document understanding**: upload a PDF (up to 10 pages) or image (PNG/JPG) and extract text with Sarvam Vision
- 🎚️ Adjustable **speech speed** (0.5x – 2.0x)
- 💾 Download output as **MP3** or **WAV**
- 🎧 Auto language detection for uploaded audio
- 🎤 Supports many audio formats: `wav, mp3, m4a, aac, ogg, opus, flac, webm, mp4, aiff, amr`

## 🧠 Models Used

| Task | Sarvam Model |
|---|---|
| Speech-to-text | `saaras:v3` |
| Translation | `mayura:v1` |
| Text-to-speech | `bulbul:v3` |
| Summarization | `sarvam-105b` |
| Document OCR (Sarvam Vision) | `doc_ai.digitise` |

## 🔄 How It Works

```
Text to speech:      Text / Doc ──► Translate ──► Bulbul TTS ──► Audio
Summarize & speak:   Text / Doc ──► Summarize ──► Translate ──► Bulbul TTS ──► Audio
Translate speech:    Audio ──► Saaras STT ──► Translate ──► Bulbul TTS ──► Audio
```

## 📁 Project Structure

```
ai-agent-sarvam-ai/
├── main.py            # Streamlit app (UI + Sarvam AI logic)
├── requirements.txt   # Python dependencies
└── .gitignore
```

## 🛠️ Getting Started

### Prerequisites

- Python 3.9+
- A Sarvam AI API key — get one from the [Sarvam AI dashboard](https://dashboard.sarvam.ai/)

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/ai-agent-sarvam-ai.git
cd ai-agent-sarvam-ai
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate      # macOS / Linux
.venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your API key

**Option A: environment variable**

```bash
export SARVAM_API_KEY="your_api_key_here"        # macOS / Linux
set SARVAM_API_KEY=your_api_key_here             # Windows (cmd)
$env:SARVAM_API_KEY="your_api_key_here"          # Windows (PowerShell)
```

**Option B: Streamlit secrets**

Create `.streamlit/secrets.toml`:

```toml
SARVAM_API_KEY = "your_api_key_here"
```

> ⚠️ `.streamlit/secrets.toml` is already in `.gitignore`. Never commit your API key.

### 5. Run the app

```bash
streamlit run main.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

## ☁️ Deploy on Streamlit Community Cloud

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and create a new app pointing to `main.py`.
3. Under **Advanced settings → Secrets**, add:
   ```toml
   SARVAM_API_KEY = "your_api_key_here"
   ```
4. Click **Deploy**.

## 📖 Usage Guide

1. Pick a **workflow** (Text to speech, Summarize & speak, or Translate speech).
2. Choose the **output language**.
3. Provide input: text, a PDF/image, or an audio file.
4. Select a **voice**, **speech speed**, and **audio format**.
5. Click the action button, then listen in the player or download the file.

## ⚠️ Limitations

- Text-to-speech input is limited to **2,500 characters** per request (Bulbul v3). Use **Summarize & speak** for longer content.
- PDFs are limited to **10 pages**; document processing times out after **3 minutes**.
- TTS output is available in **11 languages** (input/translation supports more).
- Requires a valid Sarvam AI API key and is subject to your plan's usage limits.

## 🧰 Tech Stack

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Sarvam AI Python SDK](https://pypi.org/project/sarvamai/) (`sarvamai==0.1.34`)

## 🤝 Contributing

Contributions are welcome!

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m "Add amazing feature"`
4. Push the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License. Add a `LICENSE` file to your repo if you haven't already.

## 🙏 Acknowledgements

- [Sarvam AI](https://www.sarvam.ai/) for the speech, translation, vision, and language models
- [Streamlit](https://streamlit.io/) for the rapid UI framework

---

<div align="center">
Made with ❤️ for Indian languages
</div>
