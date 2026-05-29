import tempfile
from pathlib import Path
import streamlit as st
from audio_processor import validate_audio
from transcriber import transcribe
from summarizer import summarize


st.set_page_config(page_title="Smart Voice Summarizer", layout="wide")
st.title("Smart Voice Summarizer")
st.markdown("Upload an audio file to get a transcript and bullet-point summary.")

uploaded_file = st.file_uploader(
    "Choose an audio file",
    type=["mp3", "wav", "m4a", "ogg", "flac", "mp4", "webm"],
)

if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    try:
        audio_path = validate_audio(file_bytes, uploaded_file.name)
    except ValueError as e:
        st.error(str(e))
        st.stop()

    with st.spinner("Transcribing audio..."):
        transcript = transcribe(audio_path)

    st.success(f"Detected language: **{transcript['language']}**")
    st.subheader("Transcript")
    st.write(transcript["text"])

    with st.spinner("Generating summary..."):
        result = summarize(transcript)

    st.subheader("Summary")
    st.write(result["summary"])

    st.subheader("Bullet Points")
    for point in result["bullet_points"]:
        st.write(f"- {point}")

    Path(audio_path).unlink(missing_ok=True)
