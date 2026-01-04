from typing import List, Dict, Optional
from datetime import datetime
from sqlalchemy import func

class JobService:
    """Job Management Service"""
    
    @staticmethod
    def create_job(user_id: int, job_data: Dict) -> Dict:
        """Create new job posting"""
        return {
            'id': 1,
            'recruiter_id': user_id,
            'title': job_data.get('title'),
            'company_name': job_data.get('company_name'),
            'description': job_data.get('description'),
            'required_skills': job_data.get('required_skills', []),
            'salary_min': job_data.get('salary_min'),
            'salary_max': job_data.get('salary_max'),
            'seniority_level': job_data.get('seniority_level'),
            'location': job_data.get('location'),
            'work_mode': job_data.get('work_mode', 'Hybrid'),
            'status': 'open',
            'created_at': datetime.now().isoformat()
        }
    
    @staticmethod
    def get_job(job_id: int) -> Dict:
        """Get job details"""
        return {
            'id': job_id,
            'title': 'Software Engineer',
            'company_name': 'Tech Corp',
            'salary_min': 80000,
            'salary_max': 120000,
            'status': 'open'
        }
    
    @staticmethod
    def list_jobs(user_id: int, filters: Optional[Dict] = None) -> List[Dict]:
        """List user's jobs"""
        return [
            {'id': 1, 'title': 'Python Developer', 'status': 'open'},
            {'id': 2, 'title': 'React Developer', 'status': 'open'},
            {'id': 3, 'title': 'Product Manager', 'status': 'closed'}
        ]
    
    @staticmethod
    def update_job(job_id: int, job_data: Dict) -> Dict:
        """Update existing job"""
        return {**job_data, 'id': job_id, 'updated_at': datetime.now().isoformat()}
    
    @staticmethod
    def close_job(job_id: int) -> Dict:
        """Close job posting"""
        return {'id': job_id, 'status': 'closed', 'closed_at': datetime.now().isoformat()}
