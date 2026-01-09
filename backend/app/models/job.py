from datetime import datetime
from sqlalchemy import Text, JSON, Float, DateTime, Integer, String, Boolean
from app.models import db


class Job(db.Model):
    """Job posting model."""
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(String(255), nullable=False, index=True)
    description = db.Column(Text, nullable=False)
    location = db.Column(String(120), index=True)
    required_skills = db.Column(JSON, default=list)
    experience_level = db.Column(String(50))
    salary_min = db.Column(Integer)
    salary_max = db.Column(Integer)
    company = db.Column(String(255), nullable=False, index=True)
    department = db.Column(String(120))
    remote = db.Column(Boolean, default=False)
    is_active = db.Column(Boolean, default=True, index=True)
    score = db.Column(Float, default=0.0)
    created_at = db.Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    matches = db.relationship('Match', backref='job', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Job {self.title}>'
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'company': self.company,
            'location': self.location,
            'required_skills': self.required_skills,
            'experience_level': self.experience_level,
            'salary_min': self.salary_min,
            'salary_max': self.salary_max,
            'remote': self.remote,
            'score': self.score,
            'created_at': self.created_at.isoformat(),
        }
