"""
AI Career Copilot — Backend API (FastAPI + Cohere)

Run locally:
    pip install -r requirements.txt
    export COHERE_API_KEY=your_key_here
    uvicorn backend:app --reload --port 8000

Run in Google Colab:
    See colab_backend.ipynb in this folder (uses pyngrok to expose this
    server publicly so the Streamlit app can call it).
"""

import os
from typing import Optional

import cohere
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import prompts

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

COHERE_API_KEY = os.environ.get("COHERE_API_KEY")
COHERE_MODEL = os.environ.get("COHERE_MODEL", "command-a-plus-05-2026")

app = FastAPI(title="AI Career Copilot API")

# Allow the Streamlit frontend (any origin) to call this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

co: Optional[cohere.Client] = None
if COHERE_API_KEY:
    co = cohere.Client(COHERE_API_KEY)


def get_client() -> cohere.Client:
    global co
    if co is None:
        key = os.environ.get("COHERE_API_KEY")
        if not key:
            raise HTTPException(
                status_code=500,
                detail="COHERE_API_KEY is not set on the server.",
            )
        co = cohere.Client(key)
    return co


def call_cohere(prompt: str) -> str:
    client = get_client()
    try:
        response = client.chat(model=COHERE_MODEL, message=prompt)
        return response.text
    except Exception as exc:  # surfaced to the caller as a 502
        raise HTTPException(status_code=502, detail=f"Cohere API error: {exc}")


# ---------------------------------------------------------------------------
# Request models
# ---------------------------------------------------------------------------

class ResumeOnly(BaseModel):
    resume_text: str
    job_description: str = ""


class BulletRewrite(BaseModel):
    bullet_points: str
    job_description: str = ""


class CoverLetterRequest(BaseModel):
    resume_text: str
    job_description: str
    company_name: str = ""


class AtsScoreRequest(BaseModel):
    resume_text: str
    job_description: str
    score: int


# ---------------------------------------------------------------------------
# Endpoints — one per prompt
# ---------------------------------------------------------------------------

@app.get("/")
def health_check():
    return {"status": "ok", "service": "AI Career Copilot API"}


@app.post("/resume-feedback")
def resume_feedback(req: ResumeOnly):
    prompt = prompts.resume_feedback_prompt(req.resume_text, req.job_description)
    return {"result": call_cohere(prompt)}


@app.post("/skill-gap")
def skill_gap(req: ResumeOnly):
    if not req.job_description.strip():
        raise HTTPException(status_code=400, detail="job_description is required for skill gap analysis.")
    prompt = prompts.skill_gap_prompt(req.resume_text, req.job_description)
    return {"result": call_cohere(prompt)}


@app.post("/rewrite-bullets")
def rewrite_bullets(req: BulletRewrite):
    prompt = prompts.bullet_rewriter_prompt(req.bullet_points, req.job_description)
    return {"result": call_cohere(prompt)}


@app.post("/improve-resume")
def improve_resume(req: ResumeOnly):
    prompt = prompts.full_resume_improver_prompt(req.resume_text, req.job_description)
    return {"result": call_cohere(prompt)}


@app.post("/cover-letter")
def cover_letter(req: CoverLetterRequest):
    prompt = prompts.cover_letter_prompt(req.resume_text, req.job_description, req.company_name)
    return {"result": call_cohere(prompt)}


@app.post("/interview-questions")
def interview_questions(req: ResumeOnly):
    if not req.job_description.strip():
        raise HTTPException(status_code=400, detail="job_description is required for interview questions.")
    prompt = prompts.interview_questions_prompt(req.resume_text, req.job_description)
    return {"result": call_cohere(prompt)}


@app.post("/career-suggestions")
def career_suggestions(req: ResumeOnly):
    prompt = prompts.career_suggestions_prompt(req.resume_text, req.job_description)
    return {"result": call_cohere(prompt)}


@app.post("/ats-score-explanation")
def ats_score_explanation(req: AtsScoreRequest):
    prompt = prompts.ats_score_explanation_prompt(req.resume_text, req.job_description, req.score)
    return {"result": call_cohere(prompt)}


@app.post("/final-summary")
def final_summary(req: ResumeOnly):
    prompt = prompts.final_summary_prompt(req.resume_text, req.job_description)
    return {"result": call_cohere(prompt)}
