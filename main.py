from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import httpx
import os
from io import BytesIO
from pypdf import PdfReader
from docx import Document
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

class ScreenRequest(BaseModel):
    job_description: str
    resume: str


def extract_resume_text(filename: str, file_bytes: bytes) -> str:
    lower_name = filename.lower()

    if lower_name.endswith(".pdf"):
        reader = PdfReader(BytesIO(file_bytes))
        text_parts = [(page.extract_text() or "") for page in reader.pages]
        return "\n".join(part.strip() for part in text_parts if part.strip())

    if lower_name.endswith(".docx"):
        document = Document(BytesIO(file_bytes))
        text_parts = [p.text.strip() for p in document.paragraphs if p.text.strip()]
        return "\n".join(text_parts)

    raise HTTPException(
        status_code=400,
        detail="Unsupported file type. Please upload a PDF or DOCX file."
    )


@app.post("/extract-resume")
async def extract_resume(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file selected.")

    raw = await file.read()
    if not raw:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    try:
        text = extract_resume_text(file.filename, raw)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Could not read file: {exc}")

    if not text.strip():
        raise HTTPException(status_code=400, detail="No readable text found in the file.")

    return {"resume_text": text}

@app.post("/analyze")
async def analyze(data: ScreenRequest):
    if not GROQ_API_KEY:
        raise HTTPException(status_code=500, detail="API key not configured on server.")

    prompt = f"""You are an expert technical recruiter. Analyze the following job description and candidate resume.

JOB DESCRIPTION:
{data.job_description}

CANDIDATE RESUME:
{data.resume}

Respond ONLY with a valid JSON object in this exact format (no extra text, no markdown):
{{
  "score": <number 0-100>,
  "verdict": "<one of: Strong Match / Good Match / Partial Match / Weak Match>",
  "summary": "<2-3 sentence overall assessment>",
  "hire_reasons": ["<reason 1>", "<reason 2>", "<reason 3>"],
  "red_flags": ["<flag 1>", "<flag 2>"]
}}"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 600
    }

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(GROQ_URL, json=payload, headers=headers)

    if response.status_code != 200:
        # Return the provider's message to make config/model issues visible.
        error_detail = "Groq API error."
        try:
            error_json = response.json()
            if isinstance(error_json, dict):
                message = error_json.get("error", {}).get("message")
                if message:
                    error_detail = f"Groq API error: {message}"
        except Exception:
            pass
        raise HTTPException(status_code=response.status_code, detail=error_detail)

    result = response.json()
    content = result["choices"][0]["message"]["content"].strip()
    content = content.replace("```json", "").replace("```", "").strip()

    import json
    return json.loads(content)

# Serve frontend
app.mount("/", StaticFiles(directory="static", html=True), name="static")