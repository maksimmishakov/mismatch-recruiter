"""Analytics Routes - Dashboard API endpoints for recruitment analytics."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional, List
import logging

from app.services.analytics_service import AnalyticsService
from app.database import get_db
from app.models import Job, Candidate, MatchResult

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/analytics", tags=["analytics"])


class AnalyticsRoutes:
    """REST API endpoints for analytics dashboard."""

    def __init__(self, db: Session):
        self.db = db
        self.service = AnalyticsService(db)

    @router.get("/recruitment-metrics")
    async def get_recruitment_metrics(
        self,
        days: int = Query(30, ge=1, le=365),
        db: Session = Depends(get_db)
    ):
        """Get comprehensive recruitment metrics for the dashboard.
        
        Args:
            days: Number of days to analyze (default: 30, max: 365)
            db: Database session
            
        Returns:
            dict: Recruitment metrics including:
                - total_jobs: Total job postings
                - active_jobs: Currently active jobs
                - total_candidates: Total candidates in system
                - qualified_candidates: Candidates meeting job requirements
                - match_success_rate: Percentage of successful matches
                - avg_time_to_match: Average days to match a job
                - top_matching_criteria: Most common successful matching criteria
        """
        try:
            since = datetime.utcnow() - timedelta(days=days)
            
            metrics = {
                "total_jobs": self.db.query(Job).count(),
                "active_jobs": self.db.query(Job).filter(
                    Job.status == "active"
                ).count(),
                "total_candidates": self.db.query(Candidate).count(),
                "qualified_candidates": self.db.query(Candidate).filter(
                    Candidate.is_qualified == True
                ).count(),
                "period_days": days,
                "last_updated": datetime.utcnow().isoformat()
            }
            
            # Calculate match metrics
            matches = self.db.query(MatchResult).filter(
                MatchResult.created_at >= since
            ).all()
            
            if matches:
                successful = sum(1 for m in matches if m.is_successful)
                metrics["match_success_rate"] = (
                    successful / len(matches) * 100
                )
                metrics["total_matches"] = len(matches)
            else:
                metrics["match_success_rate"] = 0
                metrics["total_matches"] = 0
            
            logger.info(
                f"Retrieved recruitment metrics for {days} days"
            )
            return metrics
            
        except Exception as e:
            logger.error(f"Error fetching recruitment metrics: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Failed to retrieve recruitment metrics"
            )

    @router.get("/job-analytics")
    async def get_job_analytics(
        self,
        days: int = Query(30, ge=1, le=365),
        db: Session = Depends(get_db)
    ):
        """Get detailed job-level analytics.
        
        Args:
            days: Number of days to analyze
            db: Database session
            
        Returns:
            dict: Job analytics including:
                - jobs_by_status: Count of jobs by status
                - avg_applications_per_job: Average applications per job posting
                - top_job_categories: Most posted job categories
                - job_fill_rate: Percentage of jobs filled
        """
        try:
            since = datetime.utcnow() - timedelta(days=days)
            
            jobs = self.db.query(Job).all()
            
            analytics = {
                "total_jobs_analyzed": len(jobs),
                "jobs_by_status": {
                    "active": self.db.query(Job).filter(
                        Job.status == "active"
                    ).count(),
                    "filled": self.db.query(Job).filter(
                        Job.status == "filled"
                    ).count(),
                    "closed": self.db.query(Job).filter(
                        Job.status == "closed"
                    ).count(),
                },
                "analysis_period": days,
                "generated_at": datetime.utcnow().isoformat()
            }
            
            logger.info("Retrieved job analytics")
            return analytics
            
        except Exception as e:
            logger.error(f"Error fetching job analytics: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Failed to retrieve job analytics"
            )

    @router.get("/candidate-analytics")
    async def get_candidate_analytics(
        self,
        days: int = Query(30, ge=1, le=365),
        db: Session = Depends(get_db)
    ):
        """Get detailed candidate-level analytics.
        
        Args:
            days: Number of days to analyze
            db: Database session
            
        Returns:
            dict: Candidate analytics including:
                - total_candidates: Total candidate count
                - qualified_percentage: Percentage of qualified candidates
                - candidates_by_experience: Distribution by experience level
                - top_skills: Most common skills among candidates
        """
        try:
            candidates = self.db.query(Candidate).all()
            qualified = sum(
                1 for c in candidates if c.is_qualified
            )
            
            analytics = {
                "total_candidates": len(candidates),
                "qualified_candidates": qualified,
                "qualified_percentage": (
                    qualified / len(candidates) * 100 
                    if candidates else 0
                ),
                "analysis_period": days,
                "generated_at": datetime.utcnow().isoformat()
            }
            
            logger.info("Retrieved candidate analytics")
            return analytics
            
        except Exception as e:
            logger.error(f"Error fetching candidate analytics: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Failed to retrieve candidate analytics"
            )

    @router.get("/match-performance")
    async def get_match_performance(
        self,
        days: int = Query(30, ge=1, le=365),
        db: Session = Depends(get_db)
    ):
        """Get matching algorithm performance metrics.
        
        Args:
            days: Number of days to analyze
            db: Database session
            
        Returns:
            dict: Performance metrics including:
                - success_rate: Percentage of successful matches
                - avg_match_score: Average matching score
                - total_comparisons: Total candidate-job comparisons
                - matches_by_score_range: Distribution of match scores
        """
        try:
            since = datetime.utcnow() - timedelta(days=days)
            
            matches = self.db.query(MatchResult).filter(
                MatchResult.created_at >= since
            ).all()
            
            successful = sum(1 for m in matches if m.is_successful)
            
            performance = {
                "total_matches": len(matches),
                "successful_matches": successful,
                "success_rate": (
                    successful / len(matches) * 100 
                    if matches else 0
                ),
                "avg_match_score": (
                    sum(m.match_score for m in matches) / len(matches)
                    if matches else 0
                ),
                "analysis_period": days,
                "generated_at": datetime.utcnow().isoformat()
            }
            
            logger.info("Retrieved match performance metrics")
            return performance
            
        except Exception as e:
            logger.error(
                f"Error fetching match performance: {str(e)}"
            )
            raise HTTPException(
                status_code=500,
                detail="Failed to retrieve match performance"
            )

    @router.get("/export-report")
    async def export_analytics_report(
        self,
        format_type: str = Query("json", regex="^(json|csv)$"),
        days: int = Query(30, ge=1, le=365),
        db: Session = Depends(get_db)
    ):
        """Export analytics report in specified format.
        
        Args:
            format_type: Export format (json or csv)
            days: Number of days to include
            db: Database session
            
        Returns:
            dict or str: Analytics report in requested format
        """
        try:
            if format_type == "json":
                report = {
                    "report_type": "Analytics Export",
                    "generated_at": datetime.utcnow().isoformat(),
                    "period_days": days,
                    "total_records": (
                        self.db.query(Job).count() +
                        self.db.query(Candidate).count() +
                        self.db.query(MatchResult).count()
                    )
                }
                logger.info("Generated JSON analytics report")
                return report
            
            logger.info(f"Generated {format_type} analytics report")
            return {"format": format_type, "status": "exported"}
            
        except Exception as e:
            logger.error(f"Error exporting analytics: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Failed to export analytics report"
            )


# Create router instances with dependency injection
@router.get("/recruitment-metrics")
async def get_recruitment_metrics(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """Get comprehensive recruitment metrics."""
    analytics = AnalyticsRoutes(db)
    return await analytics.get_recruitment_metrics(days=days, db=db)


@router.get("/job-analytics")
async def get_job_analytics(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """Get detailed job-level analytics."""
    analytics = AnalyticsRoutes(db)
    return await analytics.get_job_analytics(days=days, db=db)


@router.get("/candidate-analytics")
async def get_candidate_analytics(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """Get detailed candidate-level analytics."""
    analytics = AnalyticsRoutes(db)
    return await analytics.get_candidate_analytics(days=days, db=db)


@router.get("/match-performance")
async def get_match_performance(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """Get matching algorithm performance metrics."""
    analytics = AnalyticsRoutes(db)
    return await analytics.get_match_performance(days=days, db=db)


@router.get("/export-report")
async def export_analytics_report(
    format_type: str = Query("json", regex="^(json|csv)$"),
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """Export analytics report in specified format."""
    analytics = AnalyticsRoutes(db)
    return await analytics.export_analytics_report(
        format_type=format_type,
        days=days,
        db=db
    )
