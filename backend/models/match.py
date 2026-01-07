from app import db
from datetime import datetime

class Match(db.Model):
    __tablename__ = 'matches'
    
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), nullable=False, index=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False, index=True)
    score = db.Column(db.Float, default=0.0)
    skill_match = db.Column(db.Float, default=0.0)
    experience_match = db.Column(db.Float, default=0.0)
    salary_match = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='NEW')
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'candidate_id': self.candidate_id,
            'job_id': self.job_id,
            'score': self.score,
            'status': self.status
        }
