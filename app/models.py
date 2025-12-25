"""Database Models"""
from datetime import datetime
from app import db

class Candidate(db.Model):
    """Candidate/Resume Model"""
    __tablename__ = 'candidates'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    position = db.Column(db.String(255))
    skills = db.Column(db.JSON, default=list)
    score = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(50), default='pending')
    red_flags = db.Column(db.JSON, default=list)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'position': self.position,
            'skills': self.skills,
            'score': self.score,
            'status': self.status,
            'red_flags': self.red_flags,
            'date_added': self.date_added.isoformat() if self.date_added else None
        }

class Job(db.Model):
    """Job Posting Model"""
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    required_skills = db.Column(db.JSON, default=list)
    company = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'required_skills': self.required_skills,
            'company': self.company,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
