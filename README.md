# HireCheck - AI Resume vs Job Description Screener

HireCheck is a FastAPI-based web app that compares a job description with a candidate resume and returns a structured hiring analysis.

The app uses a Groq LLM to generate:
- Match score (0-100)
- Verdict (Strong Match / Good Match / Partial Match / Weak Match)
- Short summary
- Hire reasons
- Red flags

This project is intentionally simple, practical, and easy to demo.

## Why This Project Helps for Automation Roles

This project shows skills that are relevant for Automation Engineer, QA Automation, and API Automation roles:
- API-first backend design using FastAPI
- Structured JSON contracts between frontend and backend
- External API integration with authentication and error handling
- Config-driven development using environment variables
- Debugging and production-style troubleshooting (timeouts, invalid model, clear error messages)
- Clean separation of UI and backend logic

## Tech Stack

- Python 3.11+
- FastAPI
- Uvicorn
- Httpx
- Python-dotenv
- HTML/CSS/JS frontend (served as static files)
- Groq Chat Completions API

## Project Structure

```text
Hirecheck/
|-- main.py                # FastAPI app and /analyze endpoint
|-- requirements.txt       # Python dependencies
|-- .env                   # Secrets and model config (local only)
|-- static/
|   |-- index.html         # Frontend UI
|-- Hirecheck/             # Virtual environment folder (local)
```

## What It Does

1. User pastes a job description and resume in the UI.
2. Frontend sends both texts to POST /analyze.
3. Backend builds a recruiter-style prompt and calls Groq.
4. Backend enforces JSON output and returns parsed result.
5. UI displays score, verdict, reasons, and red flags.

## Local Setup (Windows PowerShell)

### 1) Create and activate virtual environment

```powershell
py -3.11 -m venv Hirecheck
.\Hirecheck\Scripts\Activate.ps1
```

### 2) Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 3) Configure environment variables

Create or update .env:

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

### 4) Run the app

```powershell
uvicorn main:app --reload
```

Open:
- http://127.0.0.1:8000

## API Contract

### Endpoint

- POST /analyze

### Request Body

```json
{
  "job_description": "string",
  "resume": "string"
}
```

### Success Response

```json
{
  "score": 82,
  "verdict": "Good Match",
  "summary": "Candidate aligns well with cloud, API, and backend requirements.",
  "hire_reasons": [
    "Hands-on FastAPI and Python development",
    "Relevant cloud and container exposure",
    "Good problem-solving and communication signals"
  ],
  "red_flags": [
    "Limited production-scale ownership examples",
    "Needs deeper testing framework depth"
  ]
}
```

## Common Errors and Fixes

### Groq API error: model decommissioned

Cause:
- Old model name is no longer supported.

Fix:
- Use a supported model in .env, for example:
  - GROQ_MODEL=llama-3.3-70b-versatile

### API key not configured on server

Cause:
- GROQ_API_KEY is missing in .env.

Fix:
- Add a valid Groq key and restart Uvicorn.

### pip installs globally instead of venv

Cause:
- Virtual environment not activated.

Fix:
- Activate first, then install using python -m pip.

## Security Notes

- Never commit .env or API keys.
- Rotate keys immediately if exposed.
- Keep model and key values configurable via environment variables.

## How to Present This in Interviews

Use this 30-second summary:

"I built a FastAPI-based AI screening tool that takes job descriptions and resumes, calls a production LLM API, and returns a strict JSON scoring output with reasons and red flags. I focused on API contract clarity, error handling, and config-driven deployment, which maps directly to API automation and backend automation workflows."

## Suggested Next Improvements (Automation-Focused)

- Add pytest test suite for /analyze endpoint
- Add request validation and length limits
- Add retry/backoff for external API failures
- Add structured logging and request IDs
- Add GitHub Actions CI for lint and tests
- Dockerize app for consistent deployment

## License

For learning and portfolio use.
