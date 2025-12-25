"""Database Models with Relationships and Indices"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, index=True, nullable=False)
    name = db.Column(db.String(255), index=True, nullable=False)
    password_hash = db.Column(db.String(255))
    subscription_plan = db.Column(db.String(50), default='free', index=True)
    stripe_customer_id = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    resumes = db.relationship('Resume', backref='user', lazy=True, cascade='all, delete-orphan')
    jobs = db.relationship('Job', backref='user', lazy=True, cascade='all, delete-orphan')
    
    __table_args__ = (
        db.Index('idx_user_created_subscription', 'created_at', 'subscription_plan'),
    )
    
    def to_dict(self):
        return {'id': self.id, 'email': self.email, 'name': self.name}

class Resume(db.Model):
    __tablename__ = 'resumes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    name = db.Column(db.String(255), index=True, nullable=False)
    email = db.Column(db.String(255), index=True, nullable=False)
    skills = db.Column(db.JSON)
    experience_years = db.Column(db.Integer, index=True)
    location = db.Column(db.String(100), index=True)
    summary = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    matches = db.relationship('Match', backref='resume', lazy=True, cascade='all, delete-orphan')
    
    __table_args__ = (
        db.Index('idx_resume_user_created', 'user_id', 'created_at'),
        db.Index('idx_resume_skills_location', 'location'),
    )
    
    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'email': self.email, 'skills': self.skills}

class Job(db.Model):
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    title = db.Column(db.String(255), index=True, nullable=False)
    company = db.Column(db.String(255), index=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    required_skills = db.Column(db.JSON)
    salary_min = db.Column(db.Integer, index=True)
    salary_max = db.Column(db.Integer, index=True)
    location = db.Column(db.String(100), index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    matches = db.relationship('Match', backref='job', lazy=True, cascade='all, delete-orphan')
    
    __table_args__ = (
        db.Index('idx_job_user_created', 'user_id', 'created_at'),
        db.Index('idx_job_company_salary', 'company', 'salary_min'),
        db.Index('idx_job_title_location', 'title', 'location'),
    )
    
    def to_dict(self):
        return {'id': self.id, 'title': self.title, 'company': self.company, 'salary_min': self.salary_min}

class Match(db.Model):
    __tablename__ = 'matches'
    
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=False, index=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False, index=True)
    match_score = db.Column(db.Float, index=True)
    semantic_fit = db.Column(db.String(50))
    skill_gap_percentage = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    __table_args__ = (
        db.UniqueConstraint('resume_id', 'job_id', name='uq_resume_job'),
        db.Index('idx_match_score_created', 'match_score', 'created_at'),
    )
    
    def to_dict(self):
        return {'id': self.id, 'match_score': self.match_score, 'skill_gap': self.skill_gap_percentage}

class Prediction(db.Model):
    __tablename__ = 'predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=False, index=True)
    prediction_type = db.Column(db.String(50), index=True)
    result = db.Column(db.JSON)
    confidence = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    __table_args__ = (
        db.Index('idx_prediction_type_created', 'prediction_type', 'created_at'),
    )
    
    def to_dict(self):
        return {'id': self.id, 'type': self.prediction_type, 'result': self.result, 'confidence': self.confidence}

class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True, index=True)
    plan = db.Column(db.String(50), default='starter')
    stripe_subscription_id = db.Column(db.String(255))
    status = db.Column(db.String(50), default='active', index=True)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    ends_at = db.Column(db.DateTime)
    
    __table_args__ = (
        db.Index('idx_subscription_status_plan', 'status', 'plan'),
    )
    
    def to_dict(self):
        return {'user_id': self.user_id, 'plan': self.plan, 'status': self.status}
