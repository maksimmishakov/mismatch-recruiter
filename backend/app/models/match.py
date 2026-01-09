from datetime import datetime
from sqlalchemy import Float, DateTime, Integer, ForeignKey, String, JSON
from app.models import db


class Match(db.Model):
    """Match model for candidate-job matches."""
    __tablename__ = 'matches'
    
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(Integer, ForeignKey('candidates.id'), nullable=False, index=True)
    job_id = db.Column(Integer, ForeignKey('jobs.id'), nullable=False, index=True)
    
    overall_score = db.Column(Float, nullable=False)
    skills_score = db.Column(Float, default=0.0)
    experience_score = db.Column(Float, default=0.0)
    location_score = db.Column(Float, default=0.0)
    salary_score = db.Column(Float, default=0.0)
    education_score = db.Column(Float, default=0.0)
    culture_score = db.Column(Float, default=0.0)
    
    matched_skills = db.Column(JSON, default=list)
    missing_skills = db.Column(JSON, default=list)
    match_reason = db.Column(String(500))
    status = db.Column(String(50), default='pending')
    notes = db.Column(String(1000))
    
    created_at = db.Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        db.Index('idx_candidate_job', 'candidate_id', 'job_id', unique=True),
        db.Index('idx_match_score', 'overall_score'),
    )
    
    def __repr__(self):
        return f'<Match C{self.candidate_id} -> J{self.job_id}>'
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'candidate_id': self.candidate_id,
            'job_id': self.job_id,
            'overall_score': self.overall_score,
            'skills_score': self.skills_score,
            'experience_score': self.experience_score,
            'location_score': self.location_score,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
        }
