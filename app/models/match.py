from datetime import datetime
from app import db

class Match(db.Model):
    """Match model for candidate-job matches"""
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id', ondelete='CASCADE'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id', ondelete='CASCADE'), nullable=False)
    match_score = db.Column(db.Float, default=0.0)
    reasoning = db.Column(db.Text)
    matched_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='pending')  # pending, contacted, rejected, hired
    
    def to_dict(self):
        return {
            'id': self.id,
            'candidate_id': self.candidate_id,
            'job_id': self.job_id,
            'match_score': self.match_score,
            'reasoning': self.reasoning,
            'status': self.status,
            'matched_at': self.matched_at.isoformat()
        }
