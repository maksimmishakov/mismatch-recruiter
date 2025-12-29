""Mismatch Integration Database Models

Defines SQLAlchemy ORM models for Mismatch API data persistence,
including jobs, candidates, placements, and sync tracking.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MismatchJob(Base):
    """Mismatch Job Listing Model"""
    __tablename__ = "Mismatch_jobs"
    
    id = Column(Integer, primary_key=True)
    Mismatch_id = Column(String(100), unique=True, index=True, nullable=False)
    title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    description = Column(Text)
    location = Column(String(100))
    salary_min = Column(Integer)
    salary_max = Column(Integer)
    currency = Column(String(3), default="RUB")
    employment_type = Column(String(50))  # full_time, part_time, contract, internship
    experience_level = Column(String(50))  # junior, mid, senior
    skills = Column(JSON)  # List of required skills
    requirements = Column(Text)
    benefits = Column(Text)
    posted_at = Column(DateTime, default=datetime.utcnow)
    external_url = Column(String(500))
    synced_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<MismatchJob(Mismatch_id={self.Mismatch_id}, title={self.title})>"


class MismatchCandidate(Base):
    """Mismatch Candidate Profile Model"""
    __tablename__ = "Mismatch_candidates"
    
    id = Column(Integer, primary_key=True)
    Mismatch_id = Column(String(100), unique=True, index=True, nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(255), index=True)
    phone = Column(String(20))
    location = Column(String(100))
    title = Column(String(255))  # Current position
    summary = Column(Text)
    skills = Column(JSON)  # List of skills
    experience_years = Column(Integer)
    education = Column(Text)
    languages = Column(JSON)  # List of languages
    available_from = Column(DateTime)
    external_url = Column(String(500))
    synced_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<MismatchCandidate(Mismatch_id={self.Mismatch_id}, email={self.email})>"


class MismatchPlacement(Base):
    """Mismatch Job Placement Model"""
    __tablename__ = "Mismatch_placements"
    
    id = Column(Integer, primary_key=True)
    Mismatch_id = Column(String(100), unique=True, index=True)
    job_id = Column(String(100), nullable=False, index=True)
    candidate_id = Column(String(100), nullable=False, index=True)
    status = Column(String(50), default="submitted")  # submitted, viewed, rejected, accepted
    match_score = Column(Float)  # 0.0 to 1.0
    submitted_at = Column(DateTime, default=datetime.utcnow)
    responded_at = Column(DateTime)
    feedback = Column(Text)
    synced_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<MismatchPlacement(job_id={self.job_id}, candidate_id={self.candidate_id}, status={self.status})>"


class MismatchSync(Base):
    """Mismatch Sync Operation Tracking Model"""
    __tablename__ = "Mismatch_sync_operations"
    
    id = Column(Integer, primary_key=True)
    sync_type = Column(String(50), nullable=False)  # full, incremental
    status = Column(String(50), default="running")  # running, completed, failed
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    jobs_synced = Column(Integer, default=0)
    candidates_synced = Column(Integer, default=0)
    placements_synced = Column(Integer, default=0)
    errors = Column(Integer, default=0)
    error_log = Column(Text)
    duration_seconds = Column(Integer)  # Total duration in seconds
    
    def __repr__(self):
        return f"<MismatchSync(sync_type={self.sync_type}, status={self.status})>"


class LamodoIntegrationConfig(Base):
    """Mismatch Integration Configuration Storage"""
    __tablename__ = "Mismatch_config"
    
    id = Column(Integer, primary_key=True)
    config_key = Column(String(100), unique=True, nullable=False, index=True)
    config_value = Column(Text, nullable=False)
    description = Column(Text)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<MismatchIntegrationConfig(key={self.config_key})>"
