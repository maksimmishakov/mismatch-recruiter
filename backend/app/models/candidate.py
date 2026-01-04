from datetime import datetime
from backend.app import db

class Candidate(db.Model):
    __tablename__ = 'candidates'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    skills = db.Column(db.JSON)
    experience_years = db.Column(db.Integer, default=0)
    current_position = db.Column(db.String(120))
    resume_url = db.Column(db.String(255))
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id, 'name': self.name, 'email': self.email,
            'phone': self.phone, 'skills': self.skills,
            'experience_years': self.experience_years,
            'current_position': self.current_position,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }
