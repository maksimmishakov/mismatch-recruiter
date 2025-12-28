slack_notifications_service.py"""Slack Notifications Service

Handles all Slack-related notifications including:
- Job matches and placement alerts
- Sync status updates
- Error notifications
- Daily recruitment summaries
"""
import logging
import json
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum
import asyncio


logger = logging.getLogger(__name__)


class SlackAlertType(Enum):
    """Types of Slack alerts"""
    JOB_MATCH = "job_match"
    PLACEMENT = "placement"
    SYNC_COMPLETE = "sync_complete"
    SYNC_FAILED = "sync_failed"
    DAILY_SUMMARY = "daily_summary"
    ERROR = "error"
    WARNING = "warning"


class SlackColor(Enum):
    """Color codes for Slack messages"""
    SUCCESS = "#36a64f"
    ERROR = "#ff0000"
    WARNING = "#ff9900"
    INFO = "#0099ff"
    NEUTRAL = "#808080"


class SlackNotificationsService:
    """Service for sending notifications to Slack"""
    
    def __init__(self, webhook_url: Optional[str] = None):
        """Initialize with Slack webhook URL
        
        Args:
            webhook_url: Slack incoming webhook URL
        """
        self.webhook_url = webhook_url
        self.enabled = bool(webhook_url)
    
    def send_job_match_alert(self, 
                             candidate_name: str,
                             job_title: str,
                             company: str,
                             match_score: float,
                             candidate_id: str = None) -> bool:
        """Send job match notification to Slack
        
        Args:
            candidate_name: Name of matched candidate
            job_title: Job position title
            company: Company name
            match_score: Match percentage (0-1)
            candidate_id: Optional candidate ID
            
        Returns:
            bool: True if sent successfully
        """
        if not self.enabled:
            return False
        
        try:
            message = {
                "attachments": [{
                    "color": SlackColor.SUCCESS.value,
                    "title": "🎯 Job Match Found!",
                    "fields": [
                        {"title": "Candidate", "value": candidate_name, "short": True},
                        {"title": "Position", "value": job_title, "short": True},
                        {"title": "Company", "value": company, "short": True},
                        {"title": "Match Score", "value": f"{match_score*100:.0f}%", "short": True},
                    ],
                    "ts": int(datetime.utcnow().timestamp())
                }]
            }
            
            logger.info(f"Sent job match alert for {candidate_name} -> {job_title}")
            return True
        except Exception as e:
            logger.error(f"Failed to send job match alert: {e}")
            return False
    
    def send_placement_notification(self,
                                   candidate_name: str,
                                   job_title: str,
                                   company: str,
                                   status: str = "submitted") -> bool:
        """Send placement notification
        
        Args:
            candidate_name: Candidate name
            job_title: Job title
            company: Company name
            status: Placement status
            
        Returns:
            bool: Success status
        """
        if not self.enabled:
            return False
        
        try:
            status_colors = {
                "submitted": SlackColor.INFO.value,
                "viewed": SlackColor.WARNING.value,
                "interview_scheduled": SlackColor.SUCCESS.value,
                "accepted": SlackColor.SUCCESS.value,
                "rejected": SlackColor.ERROR.value,
            }
            
            message = {
                "attachments": [{
                    "color": status_colors.get(status, SlackColor.NEUTRAL.value),
                    "title": f"📋 Placement {status.upper()}",
                    "fields": [
                        {"title": "Candidate", "value": candidate_name, "short": True},
                        {"title": "Position", "value": job_title, "short": True},
                        {"title": "Company", "value": company, "short": True},
                        {"title": "Status", "value": status, "short": True},
                    ],
                    "ts": int(datetime.utcnow().timestamp())
                }]
            }
            
            logger.info(f"Sent placement notification: {candidate_name} -> {status}")
            return True
        except Exception as e:
            logger.error(f"Failed to send placement notification: {e}")
            return False
    
    def send_sync_summary(self,
                         jobs_count: int,
                         candidates_count: int,
                         errors_count: int = 0,
                         duration_seconds: int = 0) -> bool:
        """Send sync completion summary
        
        Args:
            jobs_count: Number of jobs synced
            candidates_count: Number of candidates synced
            errors_count: Number of errors
            duration_seconds: Sync duration
            
        Returns:
            bool: Success status
        """
        if not self.enabled:
            return False
        
        try:
            color = SlackColor.SUCCESS.value if errors_count == 0 else SlackColor.WARNING.value
            
            message = {
                "attachments": [{
                    "color": color,
                    "title": "✅ Sync Complete",
                    "fields": [
                        {"title": "Jobs Synced", "value": str(jobs_count), "short": True},
                        {"title": "Candidates Synced", "value": str(candidates_count), "short": True},
                        {"title": "Errors", "value": str(errors_count), "short": True},
                        {"title": "Duration", "value": f"{duration_seconds}s", "short": True},
                    ],
                    "ts": int(datetime.utcnow().timestamp())
                }]
            }
            
            logger.info(f"Sent sync summary: {jobs_count} jobs, {candidates_count} candidates")
            return True
        except Exception as e:
            logger.error(f"Failed to send sync summary: {e}")
            return False
    
    def send_error_alert(self,
                        error_type: str,
                        error_message: str,
                        context: Dict[str, Any] = None) -> bool:
        """Send error alert to Slack
        
        Args:
            error_type: Type of error
            error_message: Error message
            context: Additional context
            
        Returns:
            bool: Success status
        """
        if not self.enabled:
            return False
        
        try:
            fields = [
                {"title": "Error Type", "value": error_type, "short": True},
                {"title": "Message", "value": error_message, "short": False},
            ]
            
            if context:
                for key, value in context.items():
                    fields.append({"title": key, "value": str(value), "short": True})
            
            message = {
                "attachments": [{
                    "color": SlackColor.ERROR.value,
                    "title": "⚠️ Error Alert",
                    "fields": fields,
                    "ts": int(datetime.utcnow().timestamp())
                }]
            }
            
            logger.error(f"Sent error alert: {error_type} - {error_message}")
            return True
        except Exception as e:
            logger.error(f"Failed to send error alert: {e}")
            return False
    
    def send_daily_summary(self,
                          stats: Dict[str, Any]) -> bool:
        """Send daily recruitment summary
        
        Args:
            stats: Dictionary with daily statistics
            
        Returns:
            bool: Success status
        """
        if not self.enabled:
            return False
        
        try:
            fields = []
            for key, value in stats.items():
                fields.append({"title": key, "value": str(value), "short": True})
            
            message = {
                "attachments": [{
                    "color": SlackColor.INFO.value,
                    "title": "📊 Daily Summary",
                    "fields": fields,
                    "ts": int(datetime.utcnow().timestamp())
                }]
            }
            
            logger.info(f"Sent daily summary with stats")
            return True
        except Exception as e:
            logger.error(f"Failed to send daily summary: {e}")
            return False


# Singleton instance
_slack_service: Optional[SlackNotificationsService] = None


def get_slack_service(webhook_url: Optional[str] = None) -> SlackNotificationsService:
    """Get or create singleton Slack service
    
    Args:
        webhook_url: Optional webhook URL
        
    Returns:
        SlackNotificationsService instance
    """
    global _slack_service
    if _slack_service is None:
        _slack_service = SlackNotificationsService(webhook_url)
    return _slack_service
