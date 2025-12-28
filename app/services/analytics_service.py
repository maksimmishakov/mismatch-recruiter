"""Analytics Service for Phase 4 - Dashboard & Reporting

Provides real-time analytics tracking, reporting generation,
and KPI monitoring for the matching platform.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
from sqlalchemy import func
from app.database import SessionLocal
from app.models import Resume, Job, Match
import logging

logger = logging.getLogger(__name__)


class AnalyticsService:
    """Service for tracking and aggregating matching analytics."""
    
    def __init__(self):
        self.db = SessionLocal()
    
    # METRICS: Overview
    def get_overview_metrics(self) -> Dict:
        """Get high-level matching metrics overview."""
        try:
            total_matches = self.db.query(func.count(Match.id)).scalar() or 0
            perfect_matches = self.db.query(func.count(Match.id)).filter(
                Match.recommendation == 'PERFECT_MATCH'
            ).scalar() or 0
            good_matches = self.db.query(func.count(Match.id)).filter(
                Match.recommendation == 'GOOD_MATCH'
            ).scalar() or 0
            
            avg_score = self.db.query(func.avg(Match.final_score)).scalar() or 0.0
            success_rate = (perfect_matches + good_matches) / total_matches * 100 if total_matches > 0 else 0
            
            return {
                'total_matches': int(total_matches),
                'perfect_matches': int(perfect_matches),
                'good_matches': int(good_matches),
                'average_score': float(avg_score),
                'success_rate': float(success_rate),
                'timestamp': datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting overview metrics: {e}")
            return {}
    
    # METRICS: Pipeline
    def get_pipeline_metrics(self) -> Dict:
        """Get pipeline stage distribution."""
        try:
            metrics = {
                'sourced': self.db.query(func.count(Resume.id)).scalar() or 0,
                'screened': self.db.query(func.count(Match.id)).filter(
                    Match.recommendation.in_(['GOOD_MATCH', 'PERFECT_MATCH'])
                ).scalar() or 0,
                'timestamp': datetime.utcnow().isoformat()
            }
            return metrics
        except Exception as e:
            logger.error(f"Error getting pipeline metrics: {e}")
            return {}
    
    # METRICS: Time-to-Hire
    def get_time_metrics(self) -> Dict:
        """Get time-based metrics (screening duration, etc)."""
        try:
            matches = self.db.query(Match).all()
            if not matches:
                return {'average_screening_time_hours': 0, 'timestamp': datetime.utcnow().isoformat()}
            
            total_time = sum([
                (m.updated_at - m.created_at).total_seconds() / 3600 
                for m in matches if m.created_at and m.updated_at
            ])
            avg_time = total_time / len(matches) if len(matches) > 0 else 0
            
            return {
                'average_screening_time_hours': float(avg_time),
                'timestamp': datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting time metrics: {e}")
            return {}
    
    # METRICS: Job Performance
    def get_job_metrics(self, job_id: int) -> Dict:
        """Get metrics for specific job."""
        try:
            job = self.db.query(Job).filter(Job.id == job_id).first()
            if not job:
                return {'error': 'Job not found'}
            
            matches = self.db.query(Match).filter(Match.job_id == job_id).all()
            avg_score = sum([m.final_score for m in matches]) / len(matches) if matches else 0
            
            return {
                'job_id': job_id,
                'job_title': job.title,
                'total_candidates_matched': len(matches),
                'average_match_score': float(avg_score),
                'timestamp': datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting job metrics: {e}")
            return {}
    
    # METRICS: Candidate Performance
    def get_candidate_metrics(self, candidate_id: int) -> Dict:
        """Get metrics for specific candidate."""
        try:
            candidate = self.db.query(Resume).filter(Resume.id == candidate_id).first()
            if not candidate:
                return {'error': 'Candidate not found'}
            
            matches = self.db.query(Match).filter(Match.resume_id == candidate_id).all()
            good_matches = [m for m in matches if m.recommendation in ['GOOD_MATCH', 'PERFECT_MATCH']]
            
            return {
                'candidate_id': candidate_id,
                'candidate_name': f"{candidate.first_name} {candidate.last_name}",
                'total_job_matches': len(matches),
                'good_matches': len(good_matches),
                'average_score': float(sum([m.final_score for m in matches]) / len(matches)) if matches else 0,
                'timestamp': datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting candidate metrics: {e}")
            return {}
    
    # REPORTS: Generate Summary
    def generate_summary_report(self, days: int = 7) -> Dict:
        """Generate summary report for period."""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            recent_matches = self.db.query(Match).filter(
                Match.created_at >= cutoff_date
            ).all()
            
            return {
                'period_days': days,
                'total_matches': len(recent_matches),
                'perfect_matches': len([m for m in recent_matches if m.recommendation == 'PERFECT_MATCH']),
                'good_matches': len([m for m in recent_matches if m.recommendation == 'GOOD_MATCH']),
                'average_score': float(sum([m.final_score for m in recent_matches]) / len(recent_matches)) if recent_matches else 0,
                'generated_at': datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Error generating summary report: {e}")
            return {}
    
    def close(self):
        """Close database session."""
        if self.db:
            self.db.close()


# Export
__all__ = ['AnalyticsService']
