# Lyrics Listener App

A web app that uploads song/audio files and generates draft lyrics using local AI transcription.

## Features
- Upload audio/video files
- Local transcription with faster-whisper
- Lyrics output in the browser
- Timestamped segments

## Tech Stack
- FastAPI
- faster-whisper
- Next.js
- SQLite (planned)

## Project Structure
- `backend/` FastAPI transcription API
- `frontend/` Next.js frontend
- `uploads/` local uploaded files (ignored by git)
- `outputs/` generated output files (ignored by git)

## Run Locally

### Backend
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
