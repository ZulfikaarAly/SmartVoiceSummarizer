# Project Flow

## Overview

```
User uploads audio → app.py → validate_audio() → transcribe() → summarize() → display results
```

---

## File-by-File Flow

### `app.py` — Orchestrator (Streamlit UI)

1. User uploads an audio file via the Streamlit file uploader
2. `validate_audio(file_bytes, filename)` checks extension & size, saves to temp file
3. `transcribe(audio_path)` runs Whisper on the temp file
4. Transcript text and detected language are displayed
5. `summarize(transcript)` generates summary + bullet points
6. Summary and bullet points are displayed
7. Temp file is deleted

---

### `audio_processor.py` — Audio Validation

**`validate_audio(file_bytes, filename)`**
1. Checks file extension is in `ALLOWED_EXTENSIONS` (mp3, wav, m4a, ogg, flac, mp4, webm)
2. Checks file size ≤ 50MB
3. Saves bytes to a `NamedTemporaryFile`
4. Returns the temp file path

---

### `transcriber.py` — Whisper Transcription

**`_get_model()`** (internal)
1. Global cache check — loads model only once
2. Loads Whisper `"base"` model

**`transcribe(audio_path)`**
1. Gets Whisper model via `_get_model()`
2. Calls `model.transcribe(audio_path)`
3. Returns `{text, language, segments}` dict

---

### `summarizer.py` — Summarization

**`_get_t5()`** (internal)
1. Global cache check — loads T5-small only once
2. Loads `AutoTokenizer` and `AutoModelForSeq2SeqLM` from HuggingFace

**`_split_sentences(text)`**
1. Splits text on sentence boundaries (`. ! ?`)
2. Returns list of cleaned sentences

**`_extractive_summarize(text, num_sentences=3)`**
1. Splits text into sentences
2. Builds TF-IDF matrix and cosine similarity matrix
3. Ranks sentences by similarity score
4. Returns top 3 sentences joined as a summary

**`_extractive_bullets(text, num_points=5)`**
1. Same TF-IDF + cosine similarity scoring
2. Returns top 5 sentences as a list (bullet points)

**`summarize(transcript)`**
1. Extracts text and language from transcript
2. **If English** → T5 abstractive summarization + extractive bullets
3. **If non-English** → extractive summarization + extractive bullets
4. Returns `{summary, bullet_points, language}`
