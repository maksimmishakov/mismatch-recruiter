from .database import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    full_name = db.Column(db.String(120))
    password_hash = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    candidates = db.relationship('Candidate', backref='user', lazy=True)
    jobs = db.relationship('JobPosting', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {'id': self.id, 'email': self.email, 'username': self.username, 'full_name': self.full_name, 'created_at': self.created_at.isoformat() if self.created_at else None}

class Candidate(db.Model):
    __tablename__ = 'candidates'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    skills = db.Column(db.JSON, default=list)
    experience_years = db.Column(db.Integer, default=0)
    github_url = db.Column(db.String(255))
    linkedin_url = db.Column(db.String(255))
    resume_url = db.Column(db.String(255))
    location = db.Column(db.String(120))
    salary_expectation = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {'id': self.id, 'first_name': self.first_name, 'last_name': self.last_name, 'email': self.email, 'phone': self.phone, 'skills': self.skills, 'experience_years': self.experience_years, 'github_url': self.github_url, 'linkedin_url': self.linkedin_url, 'resume_url': self.resume_url, 'location': self.location, 'salary_expectation': self.salary_expectation, 'user_id': self.user_id, 'created_at': self.created_at.isoformat() if self.created_at else None, 'updated_at': self.updated_at.isoformat() if self.updated_at else None}

class JobPosting(db.Model):
    __tablename__ = 'job_postings'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    company = db.Column(db.String(120))
    location = db.Column(db.String(120))
    min_salary = db.Column(db.Integer, default=0)
    max_salary = db.Column(db.Integer, default=0)
    required_skills = db.Column(db.JSON, default=list)
    min_experience = db.Column(db.Integer, default=0)
    experience_level = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {'id': self.id, 'title': self.title, 'description': self.description, 'company': self.company, 'location': self.location, 'min_salary': self.min_salary, 'max_salary': self.max_salary, 'required_skills': self.required_skills, 'min_experience': self.min_experience, 'experience_level': self.experience_level, 'user_id': self.user_id, 'created_at': self.created_at.isoformat() if self.created_at else None, 'updated_at': self.updated_at.isoformat() if self.updated_at else None}

class Match(db.Model):
    __tablename__ = 'matches'
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), nullable=False)
    job_posting_id = db.Column(db.Integer, db.ForeignKey('job_postings.id'), nullable=False)
    match_score = db.Column(db.Float, default=0.0)
    skill_match = db.Column(db.Float, default=0.0)
    experience_match = db.Column(db.Float, default=0.0)
    salary_match = db.Column(db.Float, default=0.0)
    location_match = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {'id': self.id, 'candidate_id': self.candidate_id, 'job_posting_id': self.job_posting_id, 'match_score': self.match_score, 'skill_match': self.skill_match, 'experience_match': self.experience_match, 'salary_match': self.salary_match, 'location_match': self.location_match, 'status': self.status, 'created_at': self.created_at.isoformat() if self.created_at else None, 'updated_at': self.updated_at.isoformat() if self.updated_at else None}
