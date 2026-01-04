from datetime import datetime
from backend.app import db

class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    required_skills = db.Column(db.JSON)
    required_experience = db.Column(db.Integer, default=0)
    salary_min = db.Column(db.Integer)
    salary_max = db.Column(db.Integer)
    location = db.Column(db.String(120))
    company = db.Column(db.String(120))
    status = db.Column(db.String(20), default='open')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id, 'title': self.title, 'description': self.description,
            'required_skills': self.required_skills,
            'required_experience': self.required_experience,
            'salary_min': self.salary_min, 'salary_max': self.salary_max,
            'location': self.location, 'company': self.company,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }
