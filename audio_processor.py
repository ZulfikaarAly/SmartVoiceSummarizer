import subprocess
import tempfile
import os
from pathlib import Path
ALLOWED_EXTENSIONS={".mp3",".wav",".m4a",".ogg",".flac",".mp4",".webm"}
MAX_FILE_SIZE=50*1024*1024

def validate_audio(file_bytes:bytes,filename:str)->str:
    ext=Path(filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Unsupported file extension: {ext}")
    if len(file_bytes) > MAX_FILE_SIZE:
        raise ValueError("File size exceeds maximum allowed size")
    # save bytes to a temporary file and return its path
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
    try:
        tmp.write(file_bytes)
        tmp.flush()
    finally:
        tmp.close()
    return tmp.name
        