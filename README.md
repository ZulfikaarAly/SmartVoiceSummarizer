# Smart Voice Summarizer

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://smartvoicesummarizer-uyvhy6sl8bqhv2tkuvf9ba.streamlit.app/)

A Streamlit-based web app that transcribes audio files using **OpenAI Whisper** and generates concise summaries using **T5-small** (abstractive) and **TF-IDF with cosine similarity** (extractive) NLP models.

## Features

- **Audio Transcription** — Uses OpenAI Whisper to transcribe speech from audio files
- **Smart Summarization** — Abstractive summarization via T5-small for English; extractive fallback via TF-IDF for other languages
- **Bullet Point Extraction** — Key sentences extracted using TF-IDF ranking
- **Multi-format Support** — Accepts mp3, wav, m4a, ogg, flac, mp4, webm
- **Clean Web UI** — Built with Streamlit for easy upload and review

## Requirements

- Python 3.8+
- [ffmpeg](https://ffmpeg.org/) (required by Whisper for audio decoding)

## Installation

```bash
# Clone the repo
git clone https://github.com/ZulfikaarAly/SmartVoiceSummarizer.git
cd SmartVoiceSummarizer

# Install Python dependencies
pip install -r requirements.txt
```

## Usage

```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser, upload an audio file, and view the transcript and summarized results.

## Project Structure

```
├── app.py              # Streamlit UI and orchestration
├── audio_processor.py  # Audio validation and temp file handling
├── transcriber.py      # Whisper transcription wrapper
├── summarizer.py       # T5 & TF-IDF summarization logic
├── requirements.txt    # Python dependencies
└── README.md           # This file
```
