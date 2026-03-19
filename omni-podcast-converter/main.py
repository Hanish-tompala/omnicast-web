import os
import uuid
import sqlite3
import json
import io
from datetime import datetime
import fitz  # PyMuPDF
from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi
import urllib.parse as urlparse
import requests
from openai import OpenAI
from dotenv import load_dotenv

# Try to import new libraries
try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

try:
    from faster_whisper import WhisperModel
except ImportError:
    WhisperModel = None

try:
    from pydub import AudioSegment
except ImportError:
    AudioSegment = None

load_dotenv()

app = FastAPI(title="OmniCast Backend V2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Download placeholder BGM if needed
bgm_path = "static/bgm.mp3"
if not os.path.exists(bgm_path):
    try:
        r = requests.get("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
        with open(bgm_path, "wb") as f: f.write(r.content)
    except: pass

# --- DB SETUP ---
def init_db():
    conn = sqlite3.connect("podcasts.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS podcasts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT,
                  transcript TEXT,
                  audio_url TEXT,
                  created_at TEXT,
                  chapters TEXT)''')
    # Try updating existing table to add chapters
    try:
        c.execute("ALTER TABLE podcasts ADD COLUMN chapters TEXT")
    except:
        pass
    conn.commit()
    conn.close()

init_db()

def save_podcast(title: str, transcript: str, audio_url: str, chapters: list = None):
    conn = sqlite3.connect("podcasts.db")
    c = conn.cursor()
    created_at = datetime.now().strftime("%B %d, %Y")
    chap_str = json.dumps(chapters) if chapters else "[]"
    c.execute("INSERT INTO podcasts (title, transcript, audio_url, created_at, chapters) VALUES (?, ?, ?, ?, ?)",
              (title, transcript, audio_url, created_at, chap_str))
    conn.commit()
    conn.close()

# --- MODELS ---
class ConversionRequest(BaseModel):
    url: str
    style: str
    language: str
    voice_id: str

class PromptRequest(BaseModel):
    prompt: str
    style: str
    language: str
    voice_id: str

class ChatRequest(BaseModel):
    podcast_id: int
    question: str

# --- AUDIO & SCRIPT RULES ---
def get_guest_voice(host_voice_id: str) -> str:
    contrasts = {
        "en-US-marcus": "en-UK-hazel",
        "en-US-terrell": "en-US-natalie",
        "en-US-miles": "en-UK-hazel",
        "en-UK-hazel": "en-US-marcus",
        "en-US-natalie": "en-US-terrell"
    }
    return contrasts.get(host_voice_id, "en-US-natalie")

def get_system_prompt_for_style(style: str, language: str) -> str:
    base = f"The script must be entirely in {language}. "
    chapters = "\nCRITICAL: Include EXACTLY 3 section breaks strictly formatted as [CHAPTER: Section Name] on their own line."
    
    if "2-Person" in style:
        return base + f"""You are an expert audio producer creating a TWO-PERSON podcast script. Style: {style}.
        RULES:
        1. Format as back-and-forth dialogue.
        2. Every spoken line MUST start with exactly "[HOST]:" or exactly "[GUEST]:".
        3. Do not include stage directions or emojis.
        4. Keep total script under 600 characters.{chapters}"""
    else:
        return base + f"""You are an expert audio producer. Adopt the persona: {style}.
        RULES:
        1. Write it as a SINGLE-SPEAKER narrative or monologue.
        2. DO NOT include speaker labels, stage directions, or emojis.
        3. Keep total script under 600 characters.{chapters}"""

def rewrite_for_audio(raw_text: str, style: str, language: str) -> str:
    nvidia_api_key = os.getenv("NVIDIA_API_KEY")
    client = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=nvidia_api_key)
    system_prompt = get_system_prompt_for_style(style, language)
    
    completion = client.chat.completions.create(
        model="meta/llama-3.1-70b-instruct",
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": f"RAW TEXT:\n{raw_text[:4000]}"}],
        temperature=0.7, max_tokens=400
    )
    return completion.choices[0].message.content.strip()

def generate_story_for_audio(prompt: str, style: str, language: str) -> str:
    nvidia_api_key = os.getenv("NVIDIA_API_KEY")
    client = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=nvidia_api_key)
    system_prompt = get_system_prompt_for_style(style, language)

    completion = client.chat.completions.create(
        model="meta/llama-3.1-70b-instruct",
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": f"PROMPT: {prompt}"}],
        temperature=0.8, max_tokens=400
    )
    return completion.choices[0].message.content.strip()

def generate_murf_audio_clip(text: str, voice_id: str) -> bytes:
    murf_api_key = os.getenv("MURF_API_KEY")
    murf_url = "https://api.murf.ai/v1/speech/generate"
    payload = {"voiceId": voice_id, "style": "Conversational", "text": text, "rate": 0, "pitch": 0, "sampleRate": 44100, "format": "MP3", "channelType": "MONO"}
    headers = {"Content-Type": "application/json", "Accept": "application/json", "api-key": murf_api_key}
    
    res = requests.post(murf_url, json=payload, headers=headers)
    if res.status_code != 200: raise HTTPException(status_code=res.status_code, detail=f"Murf Error: {res.text}")
    return requests.get(res.json().get("audioFile")).content

def process_dialogue_and_stitch(script_text: str, host_voice_id: str):
    guest_voice_id = get_guest_voice(host_voice_id)
    lines = script_text.split('\n')
    
    chapters = []
    current_ms = 0
    final_audio = AudioSegment.empty() if AudioSegment else b""
    
    combined_mp3 = b""

    for line in lines:
        line = line.strip()
        if not line: continue
            
        if line.startswith("[CHAPTER:"):
            title = line.replace("[CHAPTER:", "").replace("]", "").strip()
            chapters.append({"title": title, "start_time": current_ms / 1000.0})
            continue

        clip_bytes = None
        if line.startswith("[HOST]:"):
            text = line.replace("[HOST]:", "").strip()
            if text: clip_bytes = generate_murf_audio_clip(text, host_voice_id)
        elif line.startswith("[GUEST]:"):
            text = line.replace("[GUEST]:", "").strip()
            if text: clip_bytes = generate_murf_audio_clip(text, guest_voice_id)
        else:
            clip_bytes = generate_murf_audio_clip(line, host_voice_id)
            
        if clip_bytes:
            if AudioSegment:
                segment = AudioSegment.from_mp3(io.BytesIO(clip_bytes))
                final_audio += segment
                current_ms += len(segment)
            else:
                combined_mp3 += clip_bytes

    filename = f"podcast_{uuid.uuid4().hex}.mp3"
    filepath = os.path.join("static", filename)
    
    if AudioSegment:
        # BGM Overlay
        if os.path.exists("static/bgm.mp3"):
            bgm = AudioSegment.from_mp3("static/bgm.mp3") - 15  # reduce volume
            bgm = bgm * (len(final_audio) // len(bgm) + 1)
            bgm = bgm[:len(final_audio)]
            final_audio = final_audio.overlay(bgm)
        final_audio.export(filepath, format="mp3")
    else:
        with open(filepath, "wb") as f: f.write(combined_mp3)
        
    return f"http://localhost:8000/static/{filename}", chapters

# --- ENDPOINTS ---
@app.post("/api/convert")
async def process_youtube(request: ConversionRequest):
    try:
        vid = request.url.split("/")[-1].split("?")[0] if "youtu.be" in request.url else urlparse.parse_qs(urlparse.urlparse(request.url).query).get("v", [None])[0]
        if not vid: raise HTTPException(status_code=400, detail="Invalid YouTube URL.")
        raw_text = " ".join([chunk.text for chunk in YouTubeTranscriptApi().fetch(vid)])
        script = rewrite_for_audio(raw_text, request.style, request.language)
        audio_url, chapters = process_dialogue_and_stitch(script, request.voice_id)
        save_podcast("YouTube Conversion", script, audio_url, chapters)
        return {"status": "success", "transcript_preview": script, "audio_url": audio_url, "chapters": chapters}
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/convert/pdf")
async def process_pdf(file: UploadFile = File(...), style: str = Form(...), language: str = Form(...), voice_id: str = Form(...)):
    try:
        pdf_doc = fitz.open(stream=await file.read(), filetype="pdf")
        raw_text = "".join([page.get_text() for page in pdf_doc])
        if not raw_text.strip(): raise HTTPException(status_code=400, detail="Could not extract text.")
        script = rewrite_for_audio(raw_text, style, language)
        audio_url, chapters = process_dialogue_and_stitch(script, voice_id)
        save_podcast(f"Document: {file.filename}", script, audio_url, chapters)
        return {"status": "success", "transcript_preview": script, "audio_url": audio_url, "chapters": chapters}
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/convert/prompt")
async def process_prompt(request: PromptRequest):
    try:
        script = generate_story_for_audio(request.prompt, request.style, request.language)
        audio_url, chapters = process_dialogue_and_stitch(script, request.voice_id)
        save_podcast("AI Story Prompt", script, audio_url, chapters)
        return {"status": "success", "transcript_preview": script, "audio_url": audio_url, "chapters": chapters}
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/convert/web")
async def process_web(request: ConversionRequest):
    try:
        if not BeautifulSoup: raise HTTPException(status_code=500, detail="beautifulsoup4 not installed")
        html = requests.get(request.url).text
        soup = BeautifulSoup(html, 'html.parser')
        raw_text = " ".join([p.get_text() for p in soup.find_all('p')])
        if not raw_text.strip(): raise HTTPException(status_code=400, detail="Could not extract text.")
        script = rewrite_for_audio(raw_text, request.style, request.language)
        audio_url, chapters = process_dialogue_and_stitch(script, request.voice_id)
        save_podcast(f"Web Article: {request.url[:30]}", script, audio_url, chapters)
        return {"status": "success", "transcript_preview": script, "audio_url": audio_url, "chapters": chapters}
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/convert/audio")
async def process_audio(file: UploadFile = File(...), style: str = Form(...), language: str = Form(...), voice_id: str = Form(...)):
    try:
        if not WhisperModel: raise HTTPException(status_code=500, detail="faster-whisper not installed")
        temp_path = f"static/temp_{uuid.uuid4().hex}_{file.filename}"
        with open(temp_path, "wb") as f: f.write(await file.read())
        
        model = WhisperModel("tiny", device="cpu", compute_type="int8")
        segments, _ = model.transcribe(temp_path, beam_size=5)
        raw_text = " ".join([seg.text for seg in segments])
        
        if os.path.exists(temp_path): os.remove(temp_path)
        if not raw_text.strip(): raise HTTPException(status_code=400, detail="Could not extract text.")
        
        script = rewrite_for_audio(raw_text, style, language)
        audio_url, chapters = process_dialogue_and_stitch(script, voice_id)
        save_podcast(f"Raw Audio: {file.filename}", script, audio_url, chapters)
        return {"status": "success", "transcript_preview": script, "audio_url": audio_url, "chapters": chapters}
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def chat_podcast(request: ChatRequest):
    try:
        conn = sqlite3.connect("podcasts.db")
        c = conn.cursor()
        c.execute("SELECT transcript FROM podcasts WHERE id = ?", (request.podcast_id,))
        row = c.fetchone()
        conn.close()
        
        if not row: raise HTTPException(status_code=404, detail="Podcast not found.")
        transcript = row[0]
        
        client = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=os.getenv("NVIDIA_API_KEY"))
        sys_prompt = "You are a helpful assistant. Use exclusively the following podcast transcript to answer the user's question. If the answer is not in the transcript, say so.\n\nTRANSCRIPT:\n" + transcript
        completion = client.chat.completions.create(model="meta/llama-3.1-70b-instruct", messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": request.question}], temperature=0.3, max_tokens=300)
        return {"status": "success", "answer": completion.choices[0].message.content.strip()}
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/podcasts")
async def get_all_podcasts():
    try:
        conn = sqlite3.connect("podcasts.db")
        c = conn.cursor()
        c.execute("SELECT id, title, transcript, audio_url, created_at, chapters FROM podcasts ORDER BY id DESC")
        rows = c.fetchall()
        conn.close()
        podcasts = [{"id": r[0], "title": r[1], "transcript": r[2], "audio_url": r[3], "created_at": r[4], "chapters": json.loads(r[5] if r[5] else "[]")} for r in rows]
        return {"status": "success", "podcasts": podcasts}
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/podcasts/{podcast_id}")
async def delete_podcast(podcast_id: int):
    try:
        conn = sqlite3.connect("podcasts.db")
        c = conn.cursor()
        c.execute("SELECT audio_url FROM podcasts WHERE id = ?", (podcast_id,))
        row = c.fetchone()
        if row:
            filepath = os.path.join("static", row[0].split("/")[-1])
            if os.path.exists(filepath): os.remove(filepath)
        c.execute("DELETE FROM podcasts WHERE id = ?", (podcast_id,))
        conn.commit()
        conn.close()
        return {"status": "success", "message": "Deleted"}
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))
