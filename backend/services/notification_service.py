from typing import List, Dict
from datetime import datetime

class NotificationService:
    """Notification and Alert Service"""
    
    @staticmethod
    def create_notification(user_id: int, title: str, message: str, notif_type: str = 'info') -> Dict:
        """Create notification"""
        return {
            'id': 1,
            'user_id': user_id,
            'title': title,
            'message': message,
            'type': notif_type,
            'read': False,
            'created_at': datetime.now().isoformat()
        }
    
    @staticmethod
    def send_match_notification(recruiter_id: int, job_id: int, candidate_name: str, score: float) -> Dict:
        """Send match found notification"""
        return NotificationService.create_notification(
            recruiter_id,
            f'New Match Found - {candidate_name}',
            f'Matched candidate with score {score:.1f}% for job ID {job_id}',
            'match'
        )
    
    @staticmethod
    def send_job_closed_notification(recruiter_id: int, job_id: int, job_title: str) -> Dict:
        """Send job closed notification"""
        return NotificationService.create_notification(
            recruiter_id,
            f'Job Closed - {job_title}',
            f'Job ID {job_id} has been closed',
            'job_closed'
        )
    
    @staticmethod
    def get_notifications(user_id: int, unread_only: bool = False) -> List[Dict]:
        """Get user notifications"""
        return [
            {'id': 1, 'title': 'New Match', 'read': False},
            {'id': 2, 'title': 'Job Updated', 'read': False},
            {'id': 3, 'title': 'Salary Alert', 'read': True}
        ]
