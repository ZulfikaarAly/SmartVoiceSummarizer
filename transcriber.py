from typing import Any, Optional

try:
    import whisper  # type: ignore[import-not-found]
except ImportError:
    whisper = None


_model: Optional[Any] = None
def _get_model():
    global _model
    if _model is None:
        if whisper is None:
            raise ImportError(
                "The 'whisper' package is required. Install it with: pip install openai-whisper"
            )
        _model = whisper.load_model("base")
    return _model
def transcribe(audio_path: str) -> dict:
    model = _get_model()
    result = model.transcribe(audio_path)
    return {
        "text": result["text"].strip(),
        "language": result.get("language", "unknown"),
        "segments": [
            {
                "start": seg["start"],
                "end": seg["end"],
                "text": seg["text"].strip(),
            }
            for seg in result.get("segments", [])
        ],
    }