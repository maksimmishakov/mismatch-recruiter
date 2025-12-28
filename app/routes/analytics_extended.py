"""Enhanced Analytics Routes - REST API for analytics dashboard with Pydantic models."""
from fastapi import APIRouter, Query, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, List
import logging

from app.services.analytics_service import AnalyticsService
from app.database import SessionLocal, get_db
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["analytics"])
analytics_service = AnalyticsService()

# Pydantic Models for Requests/Responses
class MetricsResponse(BaseModel):
    """Response model for overview metrics"""
    total_matches: int
    success_rate: float
    avg_score: float
    time_to_hire_days: float
    class Config:
        schema_extra = {
            "example": {
                "total_matches": 150,
                "success_rate": 0.85,
                "avg_score": 0.78,
                "time_to_hire_days": 14.5
            }
        }

class PipelineMetricsResponse(BaseModel):
    """Response model for pipeline metrics"""
    sourced: int
    screened: int
    matched: int
    conversion_rate: float
    class Config:
        schema_extra = {
            "example": {
                "sourced": 500,
                "screened": 250,
                "matched": 100,
                "conversion_rate": 0.4
            }
        }

class JobMetricsResponse(BaseModel):
    """Response model for job-specific metrics"""
    job_id: int
    total_matches: int
    avg_score: float
    conversion_rate: float
    time_to_fill_days: Optional[float] = None

class CandidateMetricsResponse(BaseModel):
    """Response model for candidate metrics"""
    candidate_id: int
    total_matches: int
    success_rate: float
    avg_score: float
    
class ReportRequest(BaseModel):
    """Request model for report generation"""
    start_date: datetime
    end_date: datetime
    format: str = "json"  # json, csv, xlsx, pdf
    email: Optional[str] = None

class ReportResponse(BaseModel):
    """Response model for report generation"""
    filename: str
    message: str
    format: str
    size_kb: Optional[float] = None

# ENDPOINT 1: GET /api/analytics/overview
@router.get("/analytics/overview", response_model=MetricsResponse)
async def get_overview_metrics(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    """Get overall platform metrics
    
    Returns:
    - total_matches: Total number of matches
    - success_rate: Percentage of successful matches
    - avg_score: Average matching score (0-1)
    - time_to_hire_days: Average days to hire
    """
    try:
        metrics = analytics_service.get_overview_metrics(db, start_date, end_date)
        return MetricsResponse(**metrics)
    except Exception as e:
        logger.error(f"Error fetching overview metrics: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch metrics")

# ENDPOINT 2: GET /api/analytics/pipeline
@router.get("/analytics/pipeline", response_model=PipelineMetricsResponse)
async def get_pipeline_metrics(db: Session = Depends(get_db)):
    """Get candidate pipeline metrics
    
    Returns:
    - sourced: Number of sourced candidates
    - screened: Number of screened candidates
    - matched: Number of matched candidates
    - conversion_rate: Pipeline conversion rate (0-1)
    """
    try:
        metrics = analytics_service.get_pipeline_metrics(db)
        return PipelineMetricsResponse(**metrics)
    except Exception as e:
        logger.error(f"Error fetching pipeline metrics: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch pipeline metrics")

# ENDPOINT 3: GET /api/analytics/job/{job_id}
@router.get("/analytics/job/{job_id}", response_model=JobMetricsResponse)
async def get_job_metrics(
    job_id: int,
    db: Session = Depends(get_db)
):
    """Get performance metrics for a specific job
    
    Args:
    - job_id: Job identifier
    
    Returns:
    - job_id: Job identifier
    - total_matches: Number of matches for this job
    - avg_score: Average matching score
    - conversion_rate: Conversion rate from matches to hires
    - time_to_fill_days: Days taken to fill position
    """
    try:
        metrics = analytics_service.get_job_metrics(db, job_id)
        if not metrics:
            raise HTTPException(status_code=404, detail="Job not found")
        return JobMetricsResponse(**metrics)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching job metrics: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch job metrics")

# ENDPOINT 4: GET /api/analytics/candidate/{candidate_id}
@router.get("/analytics/candidate/{candidate_id}", response_model=CandidateMetricsResponse)
async def get_candidate_metrics(
    candidate_id: int,
    db: Session = Depends(get_db)
):
    """Get performance metrics for a specific candidate
    
    Args:
    - candidate_id: Candidate identifier
    
    Returns:
    - candidate_id: Candidate identifier
    - total_matches: Number of matches for this candidate
    - success_rate: Percentage of successful matches
    - avg_score: Average matching score
    """
    try:
        metrics = analytics_service.get_candidate_metrics(db, candidate_id)
        if not metrics:
            raise HTTPException(status_code=404, detail="Candidate not found")
        return CandidateMetricsResponse(**metrics)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching candidate metrics: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch candidate metrics")

# ENDPOINT 5: POST /api/analytics/report
@router.post("/analytics/report", response_model=ReportResponse)
async def generate_report(
    start_date: datetime = Query(...),
    end_date: datetime = Query(...),
    format: str = Query("json", regex="^(json|csv|xlsx|pdf)$"),
    email: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Generate analytics report in specified format
    
    Args:
    - start_date: Report start date
    - end_date: Report end date
    - format: Export format (json, csv, xlsx, pdf)
    - email: Optional email to send report to
    
    Returns:
    - filename: Generated report filename
    - message: Status message
    - format: Report format
    - size_kb: File size in kilobytes
    """
    try:
        analytics_data = analytics_service.generate_summary_report(db, start_date, end_date)
        
        if format == "json":
            filename = "report.json"
            message = "JSON report generated successfully"
        elif format == "csv":
            filename = analytics_service.export_to_csv(analytics_data)
            message = "CSV report exported successfully"
            if email:
                analytics_service.send_report_email(filename, email)
                message += f" and sent to {email}"
        elif format == "xlsx":
            filename = analytics_service.export_to_excel(analytics_data)
            message = "Excel report exported successfully"
            if email:
                analytics_service.send_report_email(filename, email)
                message += f" and sent to {email}"
        elif format == "pdf":
            filename = analytics_service.export_to_pdf(analytics_data)
            message = "PDF report exported successfully"
            if email:
                analytics_service.send_report_email(filename, email)
                message += f" and sent to {email}"
        
        return ReportResponse(
            filename=filename,
            message=message,
            format=format,
            size_kb=None
        )
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate report")

# Additional utility endpoint: GET /api/analytics/health
@router.get("/analytics/health")
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint for analytics service"""
    try:
        # Simple check to ensure database connection is working
        _ = analytics_service.get_overview_metrics(db)
        return {
            "status": "healthy",
            "service": "analytics",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail="Analytics service unavailable"
        )
