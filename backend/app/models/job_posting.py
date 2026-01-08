from ..database import db
from datetime import datetime

class JobPosting(db.Model):
    __tablename__ = 'job_postings'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)  # Optional
    company = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200))
    salary_min = db.Column(db.Float)
    salary_max = db.Column(db.Float)
    required_skills = db.Column(db.JSON)  # List of skills
    experience_level = db.Column(db.String(50))  # junior, mid, senior
    job_type = db.Column(db.String(50))  # full-time, part-time, contract
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'company': self.company,
            'location': self.location,
            'salary_min': self.salary_min,
            'salary_max': self.salary_max,
            'required_skills': self.required_skills,
            'experience_level': self.experience_level,
            'job_type': self.job_type,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
        }
