from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from app.database import Base


class Resume(Base):
    """Resume model for storing resume information."""
    __tablename__ = 'resumes'
    
    id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class Job(Base):
    """Job model for storing job listings."""
    __tablename__ = 'jobs'
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class Match(Base):
    """Match model for storing matching results between candidates and jobs."""
    __tablename__ = 'matches'
    
    id = Column(Integer, primary_key=True)
    resume_id = Column(Integer, ForeignKey('resumes.id'))
    job_id = Column(Integer, ForeignKey('jobs.id'))
    recommendation = Column(String)  # PERFECT_MATCH, GOOD_MATCH, POSSIBLE_MATCH, NOT_SUITABLE
    final_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
