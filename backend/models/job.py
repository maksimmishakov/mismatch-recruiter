from app import db
from datetime import datetime
import json

class Job(db.Model):
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    company = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(150), nullable=False)
    salary_min = db.Column(db.Float, nullable=True)
    salary_max = db.Column(db.Float, nullable=True)
    required_skills = db.Column(db.Text)  # JSON string
    experience_required = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='active')  # active, closed, filled
    posted_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_required_skills(self, skills_list):
        self.required_skills = json.dumps(skills_list)
    
    def get_required_skills(self):
        return json.loads(self.required_skills) if self.required_skills else []
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'company': self.company,
            'location': self.location,
            'salary_min': self.salary_min,
            'salary_max': self.salary_max,
            'required_skills': self.get_required_skills(),
            'experience_required': self.experience_required,
            'status': self.status,
            'posted_date': self.posted_date.isoformat(),
            'created_at': self.created_at.isoformat()
        }
