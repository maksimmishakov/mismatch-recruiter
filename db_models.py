from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Index

db = SQLAlchemy()

class Candidates(db.Model):
    __tablename__ = 'candidates'
    id = db.Column(db.String(36), primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    skills = db.Column(db.JSON)
    experience_years = db.Column(db.Integer)
    current_location = db.Column(db.String(255))
    salary_expectation_min = db.Column(db.Float)
    salary_expectation_max = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class JobProfiles(db.Model):
    __tablename__ = 'job_profiles'
    id = db.Column(db.String(36), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    required_skills = db.Column(db.JSON)
    salary_range_min = db.Column(db.Float)
    salary_range_max = db.Column(db.Float)
    location = db.Column(db.String(255))
    remote_type = db.Column(db.String(50))
    status = db.Column(db.String(50), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class MatchRecords(db.Model):
    __tablename__ = 'match_records'
    id = db.Column(db.String(36), primary_key=True)
    candidate_id = db.Column(db.String(36), db.ForeignKey('candidates.id'))
    job_id = db.Column(db.String(36), db.ForeignKey('job_profiles.id'))
    skills_match_score = db.Column(db.Float)
    experience_match_score = db.Column(db.Float)
    total_score = db.Column(db.Float)
    calculated_at = db.Column(db.DateTime, default=datetime.utcnow)

class SkillsTaxonomy(db.Model):
    __tablename__ = 'skills_taxonomy'
    id = db.Column(db.String(36), primary_key=True)
    skill_name = db.Column(db.String(255), unique=True)
    category = db.Column(db.String(100))
    importance_weight = db.Column(db.Float, default=1.0)

