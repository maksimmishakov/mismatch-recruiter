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


class Webhook(db.Model):
    __tablename__ = 'webhooks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    url = db.Column(db.String(2048), nullable=False)
    events = db.Column(db.JSON, default=[], nullable=False)
    is_active = db.Column(db.Boolean, default=True, index=True)
    secret = db.Column(db.String(255), nullable=False)
    retry_count = db.Column(db.Integer, default=3)
    timeout = db.Column(db.Integer, default=30)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref='webhooks', lazy=True)
    events_log = db.relationship('WebhookEvent', backref='webhook', lazy=True, cascade='all, delete-orphan')

    __table_args__ = (
        db.Index('idx_webhook_user_active', 'user_id', 'is_active'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'url': self.url,
            'events': self.events,
            'is_active': self.is_active,
            'retry_count': self.retry_count,
            'timeout': self.timeout,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class WebhookEvent(db.Model):
    __tablename__ = 'webhook_events'

    id = db.Column(db.Integer, primary_key=True)
    webhook_id = db.Column(db.Integer, db.ForeignKey('webhooks.id'), nullable=False, index=True)
    event_type = db.Column(db.String(100), nullable=False)
    payload = db.Column(db.JSON, nullable=False)
    status = db.Column(db.String(50), default='pending', index=True)
    response_code = db.Column(db.Integer)
    response_body = db.Column(db.Text)
    attempts = db.Column(db.Integer, default=0)
    next_retry = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        db.Index('idx_webhook_event_status', 'webhook_id', 'status'),
        db.Index('idx_webhook_event_type', 'event_type'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'webhook_id': self.webhook_id,
            'event_type': self.event_type,
            'status': self.status,
            'response_code': self.response_code,
            'attempts': self.attempts,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }



# Resume Parsing Models
class ParsedResume(db.Model):
    __tablename__ = 'parsed_resume'
    
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    raw_text = db.Column(db.Text(), nullable=True)
    parsing_status = db.Column(db.String(20), nullable=True)
    parsing_metadata = db.Column(JSON, nullable=True)
    error_message = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    skills = db.relationship('ResumeSkill', backref='resume', lazy=True, cascade='all, delete-orphan')
    education = db.relationship('ResumeEducation', backref='resume', lazy=True, cascade='all, delete-orphan')
    experience = db.relationship('ResumeExperience', backref='resume', lazy=True, cascade='all, delete-orphan')
    
    __table_args__ = (
        db.Index('ix_parsed_resume_job_id', 'job_id'),
        db.Index('ix_parsed_resume_status', 'parsing_status'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'job_id': self.job_id,
            'parsing_status': self.parsing_status,
            'skills': [s.to_dict() for s in self.skills],
            'education': [e.to_dict() for e in self.education],
            'experience': [ex.to_dict() for ex in self.experience],
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class ResumeSkill(db.Model):
    __tablename__ = 'resume_skill'
    
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('parsed_resume.id'), nullable=False)
    skill_name = db.Column(db.String(100), nullable=False)
    skill_category = db.Column(db.String(50), nullable=True)
    proficiency_level = db.Column(db.String(20), nullable=True)
    years_experience = db.Column(db.Float(), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    __table_args__ = (
        db.Index('ix_resume_skill_resume_id', 'resume_id'),
        db.Index('ix_resume_skill_name', 'skill_name'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'skill_name': self.skill_name,
            'skill_category': self.skill_category,
            'proficiency_level': self.proficiency_level,
            'years_experience': self.years_experience
        }


class ResumeEducation(db.Model):
    __tablename__ = 'resume_education'
    
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('parsed_resume.id'), nullable=False)
    school_name = db.Column(db.String(200), nullable=True)
    degree = db.Column(db.String(100), nullable=True)
    field_of_study = db.Column(db.String(100), nullable=True)
    start_date = db.Column(db.String(20), nullable=True)
    end_date = db.Column(db.String(20), nullable=True)
    gpa = db.Column(db.Float(), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    __table_args__ = (
        db.Index('ix_resume_education_resume_id', 'resume_id'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'school_name': self.school_name,
            'degree': self.degree,
            'field_of_study': self.field_of_study,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'gpa': self.gpa
        }


class ResumeExperience(db.Model):
    __tablename__ = 'resume_experience'
    
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('parsed_resume.id'), nullable=False)
    company_name = db.Column(db.String(200), nullable=True)
    job_title = db.Column(db.String(100), nullable=True)
    start_date = db.Column(db.String(20), nullable=True)
    end_date = db.Column(db.String(20), nullable=True)
    description = db.Column(db.Text(), nullable=True)
    duration_months = db.Column(db.Integer(), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    __table_args__ = (
        db.Index('ix_resume_experience_resume_id', 'resume_id'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'company_name': self.company_name,
            'job_title': self.job_title,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'description': self.description,
            'duration_months': self.duration_months
        }
