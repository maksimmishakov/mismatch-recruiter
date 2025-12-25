"""System maintenance and database cleanup tasks."""

import logging
from typing import Dict, Any
from celery import shared_task
from datetime import datetime, timedelta

from app.services.health_check import log_service_operation
from app.config import settings

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=2)
def cleanup_old_records(self, days_old: int = 30) -> Dict[str, Any]:
    """
    Clean up old records from the database to maintain performance.
    
    Args:
        days_old: Delete records older than this many days
        
    Returns:
        Dict with cleanup statistics
    """
    try:
        start_time = datetime.utcnow()
        
        from app import db
        from app.models import WebhookEvent, Match
        
        cutoff_date = datetime.utcnow() - timedelta(days=days_old)
        
        # Delete old webhook events
        webhook_count = WebhookEvent.query.filter(
            WebhookEvent.created_at < cutoff_date
        ).delete()
        
        # Delete old matches
        match_count = Match.query.filter(
            Match.created_at < cutoff_date
        ).delete()
        
        db.session.commit()
        
        # Log operation
        duration = (datetime.utcnow() - start_time).total_seconds()
        total_deleted = webhook_count + match_count
        
        log_service_operation(
            service="maintenance",
            operation="cleanup_old_records",
            status="success",
            duration=duration,
            metadata={"records_deleted": total_deleted, "days_old": days_old}
        )
        
        logger.info(f"Cleaned up {total_deleted} records older than {days_old} days")
        return {
            "status": "success",
            "webhook_events_deleted": webhook_count,
            "matches_deleted": match_count
        }
        
    except Exception as exc:
        logger.error(f"Error cleaning up old records: {exc}")
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=1)
def generate_reports(self, report_type: str = "daily") -> Dict[str, Any]:
    """
    Generate system reports and analytics.
    
    Args:
        report_type: Type of report (daily/weekly/monthly)
        
    Returns:
        Dict with report generation result
    """
    try:
        start_time = datetime.utcnow()
        
        from app import db
        from app.models import Job, Candidate, Match, User
        
        # Calculate time window based on report type
        if report_type == "daily":
            days_back = 1
        elif report_type == "weekly":
            days_back = 7
        elif report_type == "monthly":
            days_back = 30
        else:
            days_back = 1
        
        cutoff_date = datetime.utcnow() - timedelta(days=days_back)
        
        # Gather statistics
        total_jobs = Job.query.count()
        active_candidates = Candidate.query.filter_by(is_active=True).count()
        total_matches = Match.query.count()
        
        recent_matches = Match.query.filter(
            Match.created_at >= cutoff_date
        ).count()
        
        total_users = User.query.count()
        active_users = User.query.filter_by(is_active=True).count()
        
        # Get average match score
        from sqlalchemy import func
        avg_score = db.session.query(
            func.avg(Match.score)
        ).filter(
            Match.created_at >= cutoff_date
        ).scalar() or 0.0
        
        report_data = {
            "report_type": report_type,
            "generated_at": datetime.utcnow().isoformat(),
            "stats": {
                "total_jobs": total_jobs,
                "active_candidates": active_candidates,
                "total_matches": total_matches,
                "recent_matches": recent_matches,
                "avg_match_score": float(avg_score),
                "total_users": total_users,
                "active_users": active_users
            }
        }
        
        # Store report if needed
        _store_report(report_data)
        
        # Log operation
        duration = (datetime.utcnow() - start_time).total_seconds()
        log_service_operation(
            service="maintenance",
            operation="generate_reports",
            status="success",
            duration=duration,
            metadata={"report_type": report_type, "data_points": len(report_data)}
        )
        
        logger.info(f"Generated {report_type} report")
        return {"status": "success", **report_data}
        
    except Exception as exc:
        logger.error(f"Error generating {report_type} report: {exc}")
        raise self.retry(exc=exc)


@shared_task(bind=True)
def optimize_database(self) -> Dict[str, Any]:
    """
    Run database optimization tasks.
    
    Returns:
        Dict with optimization result
    """
    try:
        start_time = datetime.utcnow()
        
        from app import db
        from sqlalchemy import text
        
        # Vacuum database to reclaim space
        db.session.execute(text("VACUUM"))
        db.session.commit()
        
        # Analyze tables for query optimization
        db.session.execute(text("ANALYZE"))
        db.session.commit()
        
        # Log operation
        duration = (datetime.utcnow() - start_time).total_seconds()
        log_service_operation(
            service="maintenance",
            operation="optimize_database",
            status="success",
            duration=duration,
            metadata={"optimization_type": "vacuum_analyze"}
        )
        
        logger.info("Database optimization completed")
        return {"status": "success", "operation": "vacuum_analyze"}
        
    except Exception as exc:
        logger.error(f"Error optimizing database: {exc}")
        return {"status": "error", "error": str(exc)}


def _store_report(report_data: Dict[str, Any]) -> None:
    """
    Store generated report in database or file storage.
    
    Args:
        report_data: Report data to store
    """
    try:
        import json
        from pathlib import Path
        
        # Store as JSON file
        reports_dir = Path('app/reports')
        reports_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        filename = f"{report_data['report_type']}_report_{timestamp}.json"
        filepath = reports_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
        
        logger.info(f"Stored report at {filepath}")
        
    except Exception as e:
        logger.warning(f"Failed to store report: {e}")
