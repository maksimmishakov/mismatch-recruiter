from app import db
from datetime import datetime

class MismatchSync(db.Model):
    __tablename__ = 'mismatch_sync'
    
    id = db.Column(db.Integer, primary_key=True)
    sync_type = db.Column(db.String(50))  # full, incremental
    status = db.Column(db.String(50))  # pending, running, completed, failed
    completed_at = db.Column(db.DateTime)
    jobs_synced = db.Column(db.Integer, default=0)
    candidates_synced = db.Column(db.Integer, default=0)
    placement_synced = db.Column(db.Integer, default=0)
    errors = db.Column(db.Integer, default=0)
    error_log = db.Column(db.Text)
    duration_seconds = db.Column(db.Integer)  # Total duration in seconds
    
    def __repr__(self):
        return f"<MismatchSync(sync_type={self.sync_type}, status={self.status})>"

