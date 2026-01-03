"""Job Model - Job Listings and Descriptions"""
from datetime import datetime
from enum import Enum
from typing import List, Optional

class JobStatus(Enum):
    DRAFT = 'draft'
    PUBLISHED = 'published'
    CLOSED = 'closed'
    FILLED = 'filled'

class RemoteType(Enum):
    ONSITE = 'onsite'
    REMOTE = 'remote'
    HYBRID = 'hybrid'

class JobType(Enum):
    FULLTIME = 'fulltime'
    PARTTIME = 'parttime'
    CONTRACT = 'contract'

class Job:
    """Job model for job listings"""
    
    def __init__(self, title: str, description: str):
        self.title = title
        self.description = description
        self.description_vector = None  # For embeddings
        self.status = JobStatus.DRAFT
        self.remote_type = RemoteType.HYBRID
        self.job_type = JobType.FULLTIME
        self.required_skills: List[str] = []
        self.nice_to_have_skills: List[str] = []
        self.min_experience = 0
        self.max_experience = 20
        self.salary_min = None
        self.salary_max = None
        self.location = None
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.published_at = None
        self.closed_at = None
        self.views_count = 0
        self.applications_count = 0
    
    def publish(self):
        """Publish the job"""
        self.status = JobStatus.PUBLISHED
        self.published_at = datetime.utcnow()
    
    def close(self):
        """Close the job posting"""
        self.status = JobStatus.CLOSED
        self.closed_at = datetime.utcnow()
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'title': self.title,
            'description': self.description[:200] + '...' if len(self.description) > 200 else self.description,
            'status': self.status.value,
            'remote_type': self.remote_type.value,
            'required_skills': self.required_skills,
            'min_experience': self.min_experience,
            'max_experience': self.max_experience,
            'salary_min': self.salary_min,
            'salary_max': self.salary_max,
            'location': self.location,
            'applications': self.applications_count,
            'views': self.views_count,
            'published_at': self.published_at.isoformat() if self.published_at else None
        }
