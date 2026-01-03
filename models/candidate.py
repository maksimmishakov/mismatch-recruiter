"""Candidate Model - Job Applicants and Profiles"""
from datetime import datetime
from typing import List, Optional

class CandidateQuality(str):
    """Candidate quality levels"""
    EXCELLENT = 'excellent'
    GOOD = 'good'
    AVERAGE = 'average'
    POOR = 'poor'

class Candidate:
    """Candidate model for job applicants"""
    
    def __init__(self, email: str, first_name: str = None, last_name: str = None):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.phone = None
        self.location = None
        self.current_title = None
        self.years_experience = 0.0
        self.skills: List[str] = []
        self.education: List[str] = []
        self.resume_text = None
        self.resume_vector = None  # For embeddings
        self.linkedin_url = None
        self.github_url = None
        self.portfolio_url = None
        self.overall_score = 0.0  # 0-100 AI-calculated
        self.candidate_quality = CandidateQuality.AVERAGE
        self.risk_flags: List[str] = []
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.last_contacted = None
        self.source = 'direct'  # direct, linkedin, referral, lamoda, other
    
    def calculate_quality(self):
        """Calculate candidate quality based on score"""
        if self.overall_score >= 85:
            self.candidate_quality = CandidateQuality.EXCELLENT
        elif self.overall_score >= 70:
            self.candidate_quality = CandidateQuality.GOOD
        elif self.overall_score >= 50:
            self.candidate_quality = CandidateQuality.AVERAGE
        else:
            self.candidate_quality = CandidateQuality.POOR
    
    def add_risk_flag(self, flag: str):
        """Add a risk flag"""
        if flag not in self.risk_flags:
            self.risk_flags.append(flag)
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'email': self.email,
            'name': f"{self.first_name} {self.last_name}" if self.first_name else 'Unknown',
            'title': self.current_title,
            'experience_years': self.years_experience,
            'skills': self.skills,
            'location': self.location,
            'overall_score': round(self.overall_score, 2),
            'quality': self.candidate_quality,
            'risk_flags': self.risk_flags,
            'source': self.source,
            'created_at': self.created_at.isoformat()
        }
