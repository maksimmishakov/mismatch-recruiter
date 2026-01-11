from datetime import datetime
from sqlalchemy import Text, JSON, Float, DateTime, Integer, String, ForeignKey
from app.models import db


class Candidate(db.Model):
    """Candidate model for job seekers."""
    __tablename__ = 'candidates'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(String(120), nullable=False, index=True)
    email = db.Column(String(120), unique=True, nullable=False, index=True)
    phone = db.Column(String(20))
    location = db.Column(String(120), index=True)
    bio = db.Column(Text)
    skills = db.Column(JSON, default=list)
    experience_years = db.Column(Integer, default=0)
    education = db.Column(JSON, default=list)
    experience_level = db.Column(String(50))
    current_salary_expectations = db.Column(Integer)
    desired_roles = db.Column(JSON, default=list)
    github_profile = db.Column(String(255))
    linkedin_profile = db.Column(String(255))
    portfolio_url = db.Column(String(255))
    score = db.Column(Float, default=0.0)
    recruiter_id = db.Column(Integer, ForeignKey('users.id'), nullable=True)
    created_at = db.Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    matches = db.relationship('Match', backref='candidate', lazy=True, cascade='all, delete-orphan')
    
    @property
    def first_name(self):
        """Extract first name from full name."""
        if self.name:
            return self.name.split()[0]
        return None

    def __repr__(self):
        return f'<Candidate {self.name}>'
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'location': self.location,
            'skills': self.skills,
            'experience_years': self.experience_years,
            'experience_level': self.experience_level,
            'score': self.score,
            'created_at': self.created_at.isoformat(),
        }
