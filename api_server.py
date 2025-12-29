from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
import pdfplumber
import io
import requests
import json
import asyncio
from typing import Dict, List
from phase_2_yandex_gpt import MisMatchAI, SKILLS_TAXONOMY

app = FastAPI(
    title="MisMatch API",
    description="AI-Powered Recruitment Platform - Phase 2",
    version="2.0.0"
)

GITHUB_HTML_URL = "https://raw.githubusercontent.com/maksimmishakov/Mismatch-ai-recruiter/master/templates/index.html"
ai_brain = MisMatchAI()

@app.get("/", response_class=HTMLResponse)
async def get_index():
    """Serve index.html from GitHub (always fresh)"""
    try:
        response = requests.get(GITHUB_HTML_URL)
        response.raise_for_status()
        return HTMLResponse(content=response.text)
    except requests.exceptions.RequestException as e:
        return HTMLResponse(content=f"<h1>Error loading page</h1><p>{str(e)}</p>", status_code=500)

@app.post("/api/analyze-resume")
async def analyze_resume(file: UploadFile = File(...)):
    """Phase 1: Extract text from PDF
    Returns: raw text + basic metadata"""
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files allowed")
    
    try:
        contents = await file.read()
        with pdfplumber.open(io.BytesIO(contents)) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
        
        return {
            "status": "success",
            "filename": file.filename,
            "pages": len(pdf.pages),
            "text_length": len(text),
            "text_preview": text[:1000]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze-resume-ai")
async def analyze_resume_ai(file: UploadFile = File(...)):
    """Phase 2: AI-POWERED Resume Analysis
    Uses Yandex GPT to:
    1. Extract structured data from resume
    2. Identify skills, experience level, red flags
    3. Generate score and recommendations
    
    Returns:
    - status: success
    - filename: ...
    - analysis: {name, experience_years, technical_skills, ...}
    - score: 0-100
    - summary: Human-readable summary
    - recommendation: Based on score
    """
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files allowed")
    
    try:
        contents = await file.read()
        with pdfplumber.open(io.BytesIO(contents)) as pdf:
            resume_text = "".join(page.extract_text() or "" for page in pdf.pages)
        
        if not resume_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from PDF")
        
        analysis = await ai_brain.extract_resume_data(resume_text)
        score = calculate_resume_score(analysis)
        summary = generate_summary(analysis, score)
        
        return {
            "status": "success",
            "filename": file.filename,
            "analysis": analysis,
            "score": score,
            "summary": summary,
            "recommendation": get_recommendation(score)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/match-job")
async def match_with_job(request: Dict):
    """Compare resume analysis with job description
    
    Input:
    - resume_data: {...} from analyze-resume-ai
    - job_description: "Senior Backend Engineer needed..."
    
    Output:
    - overall_score: 87
    - skill_match: 85
    - experience_match: 90
    - level_match: 85
    - matching_skills: [Python, Docker, ...]
    - missing_skills: [Kubernetes]
    - recommendation: "STRONG MATCH"
    """
    try:
        resume_data = request.get("resume_data")
        job_description = request.get("job_description")
        
        if not resume_data or not job_description:
            raise HTTPException(status_code=400, detail="Missing resume_data or job_description")
        
        job_requirements = await ai_brain.extract_job_requirements(job_description)
        
        skill_match = calculate_skill_match(
            resume_data.get("technical_skills", []),
            job_requirements.get("required_skills", [])
        )
        experience_match = calculate_experience_match(
            resume_data.get("experience_years", 0),
            job_requirements.get("required_years", 0)
        )
        level_match = calculate_level_match(
            resume_data.get("experience_level", ""),
            job_requirements.get("required_level", "")
        )
        
        overall_score = (skill_match * 50 + experience_match * 30 + level_match * 20) / 100
        
        return {
            "overall_score": round(overall_score, 1),
            "skill_match": round(skill_match, 1),
            "experience_match": round(experience_match, 1),
            "level_match": round(level_match, 1),
            "matching_skills": find_matching_skills(
                resume_data.get("technical_skills", []),
                job_requirements.get("required_skills", [])
            ),
            "missing_skills": find_missing_skills(
                resume_data.get("technical_skills", []),
                job_requirements.get("required_skills", [])
            ),
            "recommendation": get_job_recommendation(overall_score)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/feedback")
async def submit_feedback(feedback: Dict):
    """Hiring manager submits feedback on candidate
    
    Input:
    - candidate_id: "ivan_smirnov_123"
    - job_id: "senior_backend_001"
    - hired: true
    - performance_rating: 4.5
    - would_hire_again: true
    - notes: "Great engineer, good fit"
    
    This data will be used for Phase 3: RankPO preference learning
    """
    try:
        return {
            "status": "feedback_recorded",
            "candidate_id": feedback.get("candidate_id"),
            "message": "Thank you! This feedback helps us improve matching."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# HELPER FUNCTIONS
def calculate_resume_score(analysis: Dict) -> int:
    """Calculate overall resume score (0-100)
    Based on:
    - Experience level (Senior high)
    - Number of technical skills
    - No red flags
    - Clear career trajectory
    """
    score = 50  # Base score
    
    level_bonuses = {'Junior': 20, 'Middle': 60, 'Senior': 85, 'Principal': 100}
    score = level_bonuses.get(analysis.get('experience_level', 'Middle'), 60)
    
    tech_skills = analysis.get('technical_skills', [])
    score += min(len(tech_skills) * 2, 20)  # Skills bonus: 2 per skill, max 20
    
    red_flags = analysis.get('red_flags', [])
    score -= len(red_flags) * 10  # Red flags penalty: -10 each
    
    return max(0, min(100, score))

def generate_summary(analysis: Dict, score: int) -> str:
    """Generate human-readable summary"""
    name = analysis.get('name', 'Unknown')
    level = analysis.get('experience_level', 'Middle')
    years = analysis.get('experience_years', 0)
    summary = analysis.get('summary', '')
    
    return f"{name} - {level} Engineer with {years} years - Score {score}/100. {summary}"

def get_recommendation(score: int) -> str:
    """Get recommendation based on score"""
    if score >= 85:
        return "STRONG - Interview immediately"
    elif score >= 70:
        return "GOOD - Consider for interview"
    elif score >= 50:
        return "FAIR - May need training"
    else:
        return "WEAK - Look for better candidates"

def calculate_skill_match(resume_skills: List[str], required_skills: List[str]) -> float:
    """Calculate skill match as percentage"""
    if not required_skills:
        return 1.0
    matching = len(set(resume_skills) & set(required_skills))
    total = len(required_skills)
    return matching / total

def calculate_experience_match(resume_years: int, required_years: int) -> float:
    """Calculate experience match"""
    if required_years == 0:
        return 1.0
    match = min(resume_years / required_years, 1.0)
    return match

def calculate_level_match(resume_level: str, required_level: str) -> float:
    """Calculate seniority level match"""
    level_order = {'Junior': 1, 'Middle': 2, 'Senior': 3, 'Principal': 4}
    resume_rank = level_order.get(resume_level, 2)
    required_rank = level_order.get(required_level, 2)
    
    if resume_rank >= required_rank:
        return 1.0
    else:
        return resume_rank / required_rank

def find_matching_skills(resume_skills: List[str], required_skills: List[str]) -> List[str]:
    """Find skills that match"""
    return list(set(resume_skills) & set(required_skills))

def find_missing_skills(resume_skills: List[str], required_skills: List[str]) -> List[str]:
    """Find skills that are missing"""
    return list(set(required_skills) - set(resume_skills))

def get_job_recommendation(score: float) -> str:
    """Get job matching recommendation"""
    if score >= 85:
        return "STRONG MATCH - Interview this candidate immediately"
    elif score >= 70:
        return "GOOD MATCH - Consider for interview with training plan"
    elif score >= 50:
        return "POSSIBLE MATCH - Can be trained, 4-6 weeks ramp"
    else:
        return "WEAK MATCH - Look for better candidates"

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "endpoints": [
            "GET / - Load HTML from GitHub",
            "POST /api/analyze-resume - Extract text from PDF",
            "POST /api/analyze-resume-ai - AI analysis with Yandex GPT",
            "POST /api/match-job - Compare with job description",
            "POST /api/feedback - Submit hiring feedback"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 MisMatch API Server - Phase 2")
    print("📍 Starting on http://127.0.0.1:8000")
    print("📚 Docs: http://127.0.0.1:8000/docs")
    print("❤️ Health: http://127.0.0.1:8000/health")
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
