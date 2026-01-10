from datetime import datetime
from sqlalchemy import String, DateTime, Enum, Integer
import enum
from . import db

class CandidateStatus(enum.Enum):
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
    HIRED = 'HIRED'
    REJECTED = 'REJECTED'

class Candidate(db.Model):
    __tablename__ = 'candidates'
    
    id = db.Column(Integer, primary_key=True)
    first_name = db.Column(String(50), nullable=False)
    last_name = db.Column(String(50), nullable=False)
    email = db.Column(String(100))
    phone = db.Column(String(20))
    status = db.Column(Enum(CandidateStatus), default=CandidateStatus.ACTIVE)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
