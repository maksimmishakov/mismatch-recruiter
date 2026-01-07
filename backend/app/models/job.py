from app import db
from datetime import datetime

class Job(db.Model):
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    required_skills = db.Column(db.JSON, default=list)
    min_experience = db.Column(db.Integer, default=0)
    max_salary = db.Column(db.Integer, nullable=True)
    min_salary = db.Column(db.Integer, nullable=True)
    location = db.Column(db.String(120), nullable=True)
    employment_type = db.Column(db.String(50), default='FULL_TIME')
    status = db.Column(db.String(20), default='OPEN')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    matches = db.relationship('Match', backref='job', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'required_skills': self.required_skills,
            'min_salary': self.min_salary,
            'max_salary': self.max_salary,
            'location': self.location,
            'status': self.status
        }
