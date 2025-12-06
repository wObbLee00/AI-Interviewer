# Libraries
import os
import tempfile
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles   # later for audio files
from openai import OpenAI
# from pydantic import Json   # not needed right now, can remove


# API key 
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("Set OPENAI_API_KEY in the environment variable")

client = OpenAI(api_key=OPENAI_API_KEY)


app = FastAPI()

# CORS (allow all origins for now; later you can restrict)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    # Return something, not pass (None)
    return {"message": "Voice bot backend running 🎙️"}


def transcribe_audio(file_path: str) -> str:
    """
    Use OpenAI Whisper to transcribe the audio file at file_path.
    """
    with open(file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="json",
        )
    # transcription.text is the final text
    return transcription.text.strip()


@app.post("/api/transcribe")
async def api_transcribe(file: UploadFile = File(...)):
    # Get the extension of the uploaded file
    original_ext = os.path.splitext(file.filename)[1]  # e.g. ".wav"
    suffix = original_ext if original_ext else ".webm"

    # 1) Save uploaded file to temp path
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = tmp.name   # <-- use the actual temp filename

    try:
        # 2) Transcribe with Whisper
        text = transcribe_audio(tmp_path)

        # 3) Return JSON response
        return JSONResponse({"transcript": text})

    finally:
        # 4) Delete the temp file
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
