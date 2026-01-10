from datetime import datetime
from sqlalchemy import String, DateTime, Enum, Integer, Float
import enum
from . import db

class JobStatus(enum.Enum):
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
    CLOSED = 'CLOSED'

class Job(db.Model):
    __tablename__ = 'jobs'
    
    id = db.Column(Integer, primary_key=True)
    title = db.Column(String(100), nullable=False)
    description = db.Column(String(1000))
    location = db.Column(String(100))
    salary_min = db.Column(Float)
    salary_max = db.Column(Float)
    status = db.Column(Enum(JobStatus), default=JobStatus.ACTIVE)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'salary_min': self.salary_min,
            'salary_max': self.salary_max,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
