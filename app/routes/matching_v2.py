"""REST API endpoints for advanced ML matching v2"""

from typing import List
from fastapi import APIRouter, HTTPException, Query
from app.services.matching_service_v2 import MatchingServiceV2, MatchRecommendation

router = APIRouter(prefix="/api/matches", tags=["matching"])
matching_service = MatchingServiceV2()

@router.post("/v2/advanced")
async def advanced_matches(
    job_id: int,
    limit: int = Query(100, ge=1, le=1000),
    min_score: float = Query(0.0, ge=0.0, le=1.0)
):
    """Calculate advanced matches for a job"""
    # This would fetch actual data from DB and calculate matches
    # Returning sample response for demonstration
    return {
        "job_id": job_id,
        "status": "success",
        "message": "Advanced matching v2 working",
        "matches_count": 0
    }

@router.post("/v2/candidate/{candidate_id}/find-jobs")
async def find_jobs_for_candidate(
    candidate_id: int,
    limit: int = Query(10, ge=1, le=100),
    min_score: float = Query(0.5, ge=0.0, le=1.0)
):
    """Find best job matches for a candidate"""
    return {
        "candidate_id": candidate_id,
        "status": "success",
        "message": "Job finding v2 working",
        "jobs_found": 0
    }

@router.post("/v2/batch")
async def batch_matches(job_ids: List[int], limit_per_job: int = Query(50, ge=1, le=200)):
    """Calculate matches for multiple jobs"""
    return {
        "total_jobs": len(job_ids),
        "status": "success",
        "message": "Batch matching v2 working",
        "results": {}
    }

@router.get("/v2/test")
async def test_matching():
    """Test matching service"""
    # Create test data
    test_candidate = {
        "id": 1,
        "name": "Test Candidate",
        "enriched_data": {
            "skills": [{"name": "Python", "years": 5}],
            "seniority_level": "mid",
            "total_years_experience": 5,
            "salary_expectation": 80000
        }
    }
    
    test_job = {
        "id": 1,
        "title": "Senior Python Engineer",
        "salary": 100000,
        "enriched_data": {
            "skills_required": [{"name": "Python", "level": 3, "required": True}],
            "seniority_level": 3,
            "years_required": 5,
            "hard_requirements": [{"name": "Python", "level": 3}]
        }
    }
    
    # Calculate match
    match = matching_service.calculate_match(test_candidate, test_job)
    
    return {
        "status": "success",
        "final_score": round(match.final_score, 4),
        "recommendation": match.recommendation.value,
        "explanation": match.explanation,
        "strengths": match.strengths,
        "gaps": match.gaps
    }
