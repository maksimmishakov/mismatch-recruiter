"""Candidate model for job candidates."""
from app import db
from datetime import datetime


class Candidate(db.Model):
    """Model for storing candidate information."""
    __tablename__ = 'candidates'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    skills = db.Column(db.JSON, default=list)
    experience_years = db.Column(db.Integer, default=0)
    bio = db.Column(db.Text, nullable=True)
    resume_url = db.Column(db.String(500), nullable=True)
    salary_expectation = db.Column(db.Integer, nullable=True)
    location = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    matches = db.relationship('Match', backref='candidate', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert candidate to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'skills': self.skills,
            'experience_years': self.experience_years,
            'bio': self.bio,
            'resume_url': self.resume_url,
            'salary_expectation': self.salary_expectation,
            'location': self.location,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
