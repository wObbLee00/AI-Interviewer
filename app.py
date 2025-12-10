# Libraries
from fastapi.staticfiles import StaticFiles
import os
import uuid
import tempfile
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles 
from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi import HTTPException

class UserMessage(BaseModel):
    text: str
class TTSRequest(BaseModel):
    text: str



# API key 
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("Set OPENAI_API_KEY in the environment variable")

client = OpenAI(api_key=OPENAI_API_KEY)


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


BASE_DIR=os.path.dirname(os.path.abspath(__file__))
STATIC_DIR=os.path.join(BASE_DIR, "static")
AUDIO_OUTPUT=os.path.join(STATIC_DIR,"output")

os.makedirs(AUDIO_OUTPUT,exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")




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
    return transcription.text.strip()

def generate_bot_reply(user_text: str) -> str:
    """
    Sends user's text to an OpenAI Chat Model and returns the assistant's reply.
    """
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a friendly voice assistant. "
                    "Always respond in clear, natural ENGLISH only. "
                    "Keep answers conversational and easy to speak aloud."
                ),
            },
            {"role": "user", "content": user_text},
        ],
    )
    return completion.choices[0].message.content.strip()



def text_to_speech_openai(text: str) -> str:
    """
    Use OpenAI TTS to generate an mp3 from text.
    Saves it in AUDIO_OUTPUT and returns the relative URL.
    """
    # 1) Clean + validate text
    text = (text or "").strip()
    if not text:
        text = "I am sorry, I did not catch that. Please try speaking again."

    # 2) Unique filename + full path
    filename = f"{uuid.uuid4().hex}.mp3"
    out_path = os.path.join(AUDIO_OUTPUT, filename)

    print("\n[OpenAI TTS] Generating audio for text:\n", text, "\n")

    # 3) Call OpenAI TTS with streaming response
    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",  # text-to-speech model
        voice="coral",            # one of the available voices
        input=text,
    ) as response:
        response.stream_to_file(out_path)

    # 4) Return URL for frontend
    audio_url = f"/static/output/{filename}"
    return audio_url





@app.post("/api/transcribe")
async def api_transcribe(file: UploadFile = File(...)):
    original_ext = os.path.splitext(file.filename)[1]  # e.g. ".wav"
    suffix = original_ext if original_ext else ".webm"
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


@app.post("/api/reply")
async def api_reply(message: UserMessage):
    reply = generate_bot_reply(message.text)
    return JSONResponse({"bot_reply": reply})


@app.post("/api/tts")
async def api_tts(payload: TTSRequest):
    text = (payload.text or "").strip()
    if not text:
        return JSONResponse({"detail": "Text cannot be empty."}, status_code=400)

    audio_url = text_to_speech_openai(text)
    return JSONResponse({"audio_url": audio_url})


@app.post("/api/talk")
async def api_talk(file: UploadFile = File(...)):
    original_ext = os.path.splitext(file.filename)[1]
    suffix = original_ext if original_ext else ".webm"

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = tmp.name

    try:
        # 1) STT
        user_text = transcribe_audio(tmp_path)
        print("\n[/api/talk] user_text:", user_text)

        # 2) LLM reply
        bot_text = generate_bot_reply(user_text)
        print("[/api/talk] bot_text:", bot_text, "\n")

        # 3) TTS (OpenAI)
        audio_url = text_to_speech_openai(bot_text)

        return JSONResponse(
            {
                "user_text": user_text,
                "bot_text": bot_text,
                "audio_url": audio_url,
            }
        )
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
