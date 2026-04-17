# HireCheck — Resume Screening Tool

HireCheck is a simple project I built to automate resume screening by comparing a candidate’s resume with a job description and generating a structured evaluation.

The idea was to reduce the manual effort of reading and comparing resumes and instead get a quick, consistent summary for decision-making.

---

## What It Does

- Takes a job description and a resume as input  
- Sends both to the backend  
- Uses an AI model to analyze the match  
- Returns a structured response including:
  - Match score  
  - Final verdict  
  - Summary  
  - Strengths (hire reasons)  
  - Weaknesses (red flags)  

---

## How It Works

1. User enters data in the UI  
2. Request is sent to the `/analyze` endpoint  
3. Backend prepares a structured prompt  
4. Calls the AI model via API  
5. Parses the response into JSON  
6. Displays the result on the frontend  

---

## Tech Stack

- Python (FastAPI) — backend  
- Uvicorn — server  
- HTML/CSS/JS — frontend  
- HTTPX — API calls  
- Groq API — AI model  
- python-dotenv — environment variables  

---

## Project Structure

Hirecheck/
│
├── main.py              # Backend logic  
├── requirements.txt  
├── .env                 # API keys (not pushed)  
│  
├── static/  
│   └── index.html       # Frontend  
│  
└── Hirecheck/           # Virtual environment  

---

## Running Locally

### 1. Create virtual environment

py -3.11 -m venv Hirecheck

### 2. Activate it

.\Hirecheck\Scripts\Activate

### 3. Install dependencies

pip install -r requirements.txt

### 4. Add `.env` file

GROQ_API_KEY=your_api_key  
MODEL=your_model  

### 5. Run the server

uvicorn main:app --reload  

---

## Why I Built This

I wanted to try building something practical using AI APIs instead of just small demos. Resume screening felt like a good use case because it’s repetitive and time-consuming in real scenarios.

This project helped me understand:
- how to structure prompts properly  
- how to handle API responses  
- how to design a simple backend flow  
- how to return consistent outputs instead of raw AI text  

---

## Future Improvements

- Support multiple resumes at once  
- Store results in a database  
- Improve scoring logic  
- Add better UI for recruiters  

---
