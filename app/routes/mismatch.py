"""Mismatch Integration Routes - Phase 5 Step 4.2
API endpoints for job management, candidate submission, and placement tracking
"""
from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from datetime import datetime
import logging
from app.services.Mismatch_api_client import MismatchAPIClient, MismatchJob, CandidateProfile, PlacementStatus

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/Mismatch", tags=["Mismatch"])

# Global client instance (would be dependency-injected in production)
Mismatch_client: Optional[MismatchAPIClient] = None


@router.post("/configure")
async def configure_Mismatch(
    api_key: str,
    api_secret: str,
    environment: str = "sandbox"
):
    """
    Configure Mismatch API credentials
    Returns: {"status": "connected", "jobs_available": N}
    """
    global Mismatch_client
    
    try:
        api_url = (
            "https://api.Mismatch.ru/v1"
            if environment == "production"
            else "https://sandbox-api.Mismatch.ru/v1"
        )
        
        Mismatch_client = MismatchAPIClient(
            api_key=api_key,
            api_secret=api_secret,
            api_url=api_url,
            environment=environment
        )
        
        # Test connection
        is_connected = await Mismatch_client.verify_connection()
        if not is_connected:
            raise HTTPException(
                status_code=401,
                detail="Failed to authenticate with Mismatch API"
            )
        
        # Get jobs count
        jobs = await Mismatch_client.get_jobs(limit=1)
        jobs_count = len(jobs) if jobs else 0
        
        logger.info(f"✅ Mismatch configured for {environment} environment")
        return {
            "status": "connected",
            "environment": environment,
            "jobs_available": jobs_count
        }
    except Exception as e:
        logger.error(f"Configuration failed: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Configuration failed: {str(e)}"
        )


@router.get("/jobs")
async def get_Mismatch_jobs(
    status: Optional[str] = "open",
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100)
):
    """
    Get available jobs from Mismatch
    Returns: List of jobs with details
    """
    if not Mismatch_client:
        raise HTTPException(
            status_code=400,
            detail="Mismatch not configured. Call /configure first"
        )
    
    try:
        jobs = await Mismatch_client.get_jobs(
            skip=skip,
            limit=limit,
            status=status
        )
        return {
            "total": len(jobs),
            "jobs": [job.to_dict() for job in jobs],
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Failed to fetch jobs: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch jobs: {str(e)}"
        )


@router.get("/jobs/{job_id}")
async def get_Mismatch_job(job_id: str):
    """
    Get specific job details from Mismatch
    Returns: Job details
    """
    if not Mismatch_client:
        raise HTTPException(
            status_code=400,
            detail="Mismatch not configured"
        )
    
    try:
        job = await Mismatch_client.get_job(job_id)
        return {
            "job": job.to_dict(),
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Failed to fetch job {job_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch job: {str(e)}"
        )


@router.post("/sync/{job_id}")
async def sync_job_to_Mismatch(
    job_id: int,
    min_score: float = 0.70
):
    """
    Submit matched candidates for a job to Mismatch
    Returns: {"submitted": N, "status": "sent"}
    """
    if not Mismatch_client:
        raise HTTPException(
            status_code=400,
            detail="Mismatch not configured"
        )
    
    try:
        # In production, fetch candidates from database
        # For now, return simulated response
        
        logger.info(f"Syncing job {job_id} to Mismatch")
        return {
            "job_id": job_id,
            "submitted": 5,  # Simulated count
            "status": "sent",
            "message": f"Submitted 5 candidates for job {job_id}"
        }
    except Exception as e:
        logger.error(f"Sync failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Sync failed: {str(e)}"
        )


@router.get("/placements")
async def get_placement_results(
    job_id: Optional[int] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None
):
    """
    Get hiring results from Mismatch
    Returns: Placements with status (hired, rejected, etc)
    """
    if not Mismatch_client:
        raise HTTPException(
            status_code=400,
            detail="Mismatch not configured"
        )
    
    try:
        # Parse dates if provided
        date_from_dt = None
        date_to_dt = None
        
        if date_from:
            date_from_dt = datetime.fromisoformat(date_from)
        if date_to:
            date_to_dt = datetime.fromisoformat(date_to)
        
        placements = await Mismatch_client.get_placements(
            job_id=str(job_id) if job_id else None,
            date_from=date_from_dt,
            date_to=date_to_dt
        )
        
        return {
            "total": len(placements),
            "placements": [
                {
                    "id": p.id,
                    "job_id": p.job_id,
                    "candidate_id": p.candidate_id,
                    "status": p.status,
                    "created_at": p.created_at.isoformat(),
                    "updated_at": p.updated_at.isoformat()
                }
                for p in placements
            ],
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Failed to fetch placements: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch placements: {str(e)}"
        )


@router.put("/placements/{placement_id}")
async def update_placement(
    placement_id: str,
    status: str,
    notes: Optional[str] = None
):
    """
    Update placement status
    Status values: hired, rejected, interview_scheduled, etc
    """
    if not Mismatch_client:
        raise HTTPException(
            status_code=400,
            detail="Mismatch not configured"
        )
    
    try:
        # Validate status
        valid_statuses = [
            PlacementStatus.HIRED.value,
            PlacementStatus.REJECTED.value,
            PlacementStatus.INTERVIEW_SCHEDULED.value,
            PlacementStatus.OFFER_SENT.value,
            PlacementStatus.CANCELLED.value
        ]
        
        if status not in valid_statuses:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
            )
        
        result = await Mismatch_client.update_placement(
            placement_id=placement_id,
            status=status,
            notes=notes
        )
        
        logger.info(f"Updated placement {placement_id} to {status}")
        return {
            "placement_id": placement_id,
            "status": status,
            "updated_at": datetime.utcnow().isoformat(),
            "message": f"Placement updated to {status}"
        }
    except Exception as e:
        logger.error(f"Update failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Update failed: {str(e)}"
        )


@router.get("/sync-status")
async def get_sync_status():
    """
    Get last sync status and statistics
    Returns: {"last_sync": datetime, "jobs_synced": N, "candidates_submitted": N}
    """
    if not Mismatch_client:
        raise HTTPException(
            status_code=400,
            detail="Mismatch not configured"
        )
    
    try:
        rate_limit = Mismatch_client.get_rate_limit_info()
        return {
            "environment": Mismatch_client.environment,
            "rate_limit": {
                "remaining": rate_limit["remaining"],
                "reset_at": rate_limit["reset_at"]
            },
            "last_check": datetime.utcnow().isoformat(),
            "status": "operational"
        }
    except Exception as e:
        logger.error(f"Status check failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Status check failed: {str(e)}"
        )


if __name__ == "__main__":
    logger.info("Mismatch routes initialized")
