# Notification Service - Real-time notifications for users

import logging
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum

logger = logging.getLogger(__name__)

class NotificationType(Enum):
    """Types of notifications in the system."""
    MATCH_FOUND = "match_found"
    MATCH_ACCEPTED = "match_accepted"
    MATCH_REJECTED = "match_rejected"
    APPLICATION_RECEIVED = "application_received"
    APPLICATION_ACCEPTED = "application_accepted"
    INTERVIEW_SCHEDULED = "interview_scheduled"
    JOB_ALERT = "job_alert"
    MESSAGE = "message"
    SYSTEM = "system"

class NotificationPriority(Enum):
    """Notification priority levels."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4

class NotificationService:
    """Service for managing user notifications."""
    
    @staticmethod
    def create_match_notification(user_id: int, match_data: Dict) -> Dict:
        """Create a notification for a new match found."""
        return {
            'type': NotificationType.MATCH_FOUND.value,
            'user_id': user_id,
            'title': 'New Match Found',
            'message': f"Great match with {match_data.get('name')} - {match_data.get('score', 0):.1f}% compatibility",
            'data': match_data,
            'priority': NotificationPriority.HIGH.value,
            'created_at': datetime.utcnow(),
            'read': False
        }
    
    @staticmethod
    def create_application_notification(user_id: int, app_data: Dict) -> Dict:
        """Create a notification for a new application."""
        return {
            'type': NotificationType.APPLICATION_RECEIVED.value,
            'user_id': user_id,
            'title': 'New Application',
            'message': f"New application from {app_data.get('candidate_name')} for {app_data.get('job_title')}",
            'data': app_data,
            'priority': NotificationPriority.HIGH.value,
            'created_at': datetime.utcnow(),
            'read': False
        }
    
    @staticmethod
    def create_job_alert_notification(user_id: int, job_data: Dict) -> Dict:
        """Create a notification for a job matching user preferences."""
        return {
            'type': NotificationType.JOB_ALERT.value,
            'user_id': user_id,
            'title': 'New Job Alert',
            'message': f"New {job_data.get('title')} position at {job_data.get('company')}",
            'data': job_data,
            'priority': NotificationPriority.MEDIUM.value,
            'created_at': datetime.utcnow(),
            'read': False
        }
    
    @staticmethod
    def create_system_notification(user_id: int, message: str) -> Dict:
        """Create a system notification."""
        return {
            'type': NotificationType.SYSTEM.value,
            'user_id': user_id,
            'title': 'System Notification',
            'message': message,
            'priority': NotificationPriority.MEDIUM.value,
            'created_at': datetime.utcnow(),
            'read': False
        }
