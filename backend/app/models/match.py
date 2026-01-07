from app import db
from datetime import datetime

class Match(db.Model):
    __tablename__ = 'matches'
    
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), nullable=False)
    job_posting_id = db.Column(db.Integer, db.ForeignKey('job_postings.id'), nullable=False)
    match_score = db.Column(db.Float)  # 0.0 to 1.0
    skill_match = db.Column(db.Float)  # Skill compatibility score
    experience_match = db.Column(db.Float)  # Experience level match
    location_match = db.Column(db.Float)  # Location preference match
    match_details = db.Column(db.JSON)  # Detailed match data
    status = db.Column(db.String(50), default='pending')  # pending, accepted, rejected, interviewed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'candidate_id': self.candidate_id,
            'job_posting_id': self.job_posting_id,
            'match_score': self.match_score,
            'skill_match': self.skill_match,
            'experience_match': self.experience_match,
            'location_match': self.location_match,
            'match_details': self.match_details,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
        }
