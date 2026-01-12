from app import db
from datetime import datetime
import json

class Candidate(db.Model):
    __tablename__ = 'candidates'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    resume_url = db.Column(db.String(255), nullable=True)
    skills = db.Column(db.Text)  # JSON string
    experience_years = db.Column(db.Integer, default=0)
    specialization = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(20), default='active')  # active, hired, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_skills(self, skills_list):
        self.skills = json.dumps(skills_list)
    
    def get_skills(self):
        return json.loads(self.skills) if self.skills else []
    
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'skills': self.get_skills(),
            'experience_years': self.experience_years,
            'specialization': self.specialization,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }
