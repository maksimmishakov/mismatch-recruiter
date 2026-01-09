"""Database models for MisMatch Recruiter."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.models.user import User, UserRole
from app.models.candidate import Candidate  
from app.models.job import Job
from app.models.match import Match

__all__ = [
    'db',
    'User', 'UserRole',
    'Candidate',
    'Job',
    'Match',
]
