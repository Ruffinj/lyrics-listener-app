from pathlib import Path
import shutil

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from faster_whisper import WhisperModel

app = FastAPI(title="Lyrics Listener API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".mp3", ".mp4", ".wav", ".m4a", ".webm"}

# Good starter choice for CPU
model = WhisperModel("small", device="cpu", compute_type="int8")

@app.get("/")
def root():
    return {"message": "Lyrics backend is running"}

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    suffix = Path(file.filename).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    saved_path = UPLOAD_DIR / file.filename

    with saved_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        segments, info = model.transcribe(
            str(saved_path),
            beam_size=5
        )

        lines = []
        segment_data = []

        for segment in segments:
            text = segment.text.strip()
            lines.append(text)
            segment_data.append({
                "start": round(segment.start, 2),
                "end": round(segment.end, 2),
                "text": text
            })

        return {
            "filename": file.filename,
            "language": info.language,
            "lyrics": "\n".join(lines),
            "segments": segment_data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
