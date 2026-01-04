from datetime import datetime
from backend.app import db

class Match(db.Model):
    __tablename__ = 'matches'
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    match_score = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='pending')
    reason = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id, 'candidate_id': self.candidate_id,
            'job_id': self.job_id, 'match_score': self.match_score,
            'status': self.status, 'reason': self.reason,
            'created_at': self.created_at.isoformat()
        }
