"""Database Models with Relationships, Indices, and Service Integration"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, index=True, nullable=False)
    name = db.Column(db.String(255), index=True, nullable=False)
    password_hash = db.Column(db.String(255))
    subscription_plan = db.Column(db.String(50), default='free', index=True)
    stripe_customer_id = db.Column(db.String(255))
    api_key = db.Column(db.String(255), unique=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True, index=True)
    
    # Relationships
    resumes = db.relationship('Resume', backref='user', lazy=True, cascade='all, delete-orphan')
    jobs = db.relationship('Job', backref='user', lazy=True, cascade='all, delete-orphan')
    subscriptions = db.relationship('Subscription', backref='user', lazy=True, cascade='all, delete-orphan')
    health_checks = db.relationship('HealthCheck', backref='user', lazy=True, cascade='all, delete-orphan')
    
    __table_args__ = (
        db.Index('idx_user_created_subscription', 'created_at', 'subscription_plan'),
        db.Index('idx_user_active', 'is_active'),
    )
    
    def to_dict(self):
        return {'id': self.id, 'email': self.email, 'name': self.name, 'subscription_plan': self.subscription_plan}


class Resume(db.Model):
    __tablename__ = 'resumes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    name = db.Column(db.String(255), index=True, nullable=False)
    email = db.Column(db.String(255), index=True, nullable=False)
    skills = db.Column(JSON)
    experience_years = db.Column(db.Integer, index=True)
    location = db.Column(db.String(100), index=True)
    summary = db.Column(db.Text)
    raw_text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    matches = db.relationship('Match', backref='resume', lazy=True, cascade='all, delete-orphan')
    predictions = db.relationship('Prediction', backref='resume', lazy=True, cascade='all, delete-orphan')
    
    __table_args__ = (
        db.Index('idx_resume_user_created', 'user_id', 'created_at'),
        db.Index('idx_resume_location', 'location'),
    )
    
    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'email': self.email, 'skills': self.skills, 'experience_years': self.experience_years}


class Job(db.Model):
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    title = db.Column(db.String(255), index=True, nullable=False)
    company = db.Column(db.String(255), index=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    required_skills = db.Column(JSON)
    salary_min = db.Column(db.Integer, index=True)
    salary_max = db.Column(db.Integer, index=True)
    location = db.Column(db.String(100), index=True)
    url = db.Column(db.String(500))
    source = db.Column(db.String(50), index=True)
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
        return {'id': self.id, 'title': self.title, 'company': self.company, 'salary_min': self.salary_min, 'location': self.location}


class Match(db.Model):
    __tablename__ = 'matches'
    
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=False, index=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False, index=True)
    match_score = db.Column(db.Float, index=True)
    semantic_fit = db.Column(db.String(50))
    skill_gap_percentage = db.Column(db.Float)
    match_details = db.Column(JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    __table_args__ = (
        db.UniqueConstraint('resume_id', 'job_id', name='uq_resume_job'),
        db.Index('idx_match_score_created', 'match_score', 'created_at'),
    )
    
    def to_dict(self):
        return {'id': self.id, 'match_score': self.match_score, 'skill_gap': self.skill_gap_percentage, 'semantic_fit': self.semantic_fit}


class Prediction(db.Model):
    __tablename__ = 'predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=False, index=True)
    prediction_type = db.Column(db.String(50), index=True)
    result = db.Column(JSON)
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
    stripe_subscription_id = db.Column(db.String(255), unique=True)
    status = db.Column(db.String(50), default='active', index=True)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    ends_at = db.Column(db.DateTime)
    renewal_date = db.Column(db.DateTime)
    
    __table_args__ = (
        db.Index('idx_subscription_status_plan', 'status', 'plan'),
    )
    
    def to_dict(self):
        return {'user_id': self.user_id, 'plan': self.plan, 'status': self.status}


class HealthCheck(db.Model):
    __tablename__ = 'health_checks'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    service_name = db.Column(db.String(100), index=True)
    status = db.Column(db.String(50), index=True)
    response_time = db.Column(db.Float)
    error_message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    __table_args__ = (
        db.Index('idx_health_check_service', 'service_name', 'created_at'),
    )
    
    def to_dict(self):
        return {'id': self.id, 'service_name': self.service_name, 'status': self.status, 'response_time': self.response_time}
