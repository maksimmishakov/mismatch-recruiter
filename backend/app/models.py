from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

# User model
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255))
    role = db.Column(db.String(20), default='user', index=True)
    is_active = db.Column(db.Boolean, default=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Candidate model with indexes
class Candidate(db.Model):
    __tablename__ = 'candidates'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), index=True)
    skills = db.Column(db.JSON)
    experience_years = db.Column(db.Integer, index=True)
    current_position = db.Column(db.String(120))
    status = db.Column(db.String(20), default='active', index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Candidate {self.name}>'

# Job model with indexes
class Job(db.Model):
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    required_skills = db.Column(db.JSON)
    required_experience = db.Column(db.Integer, index=True)
    salary_min = db.Column(db.Integer)
    salary_max = db.Column(db.Integer)
    location = db.Column(db.String(120), index=True)
    company = db.Column(db.String(120), index=True)
    status = db.Column(db.String(20), default='open', index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Job {self.title}>'

# Match model with composite indexes
class Match(db.Model):
    __tablename__ = 'matches'
    
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), nullable=False, index=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False, index=True)
    match_score = db.Column(db.Float, default=0.0, index=True)
    status = db.Column(db.String(20), default='pending', index=True)
    reason = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    candidate = db.relationship('Candidate', backref=db.backref('matches', lazy='dynamic'))
    job = db.relationship('Job', backref=db.backref('matches', lazy='dynamic'))
    
    # Composite indexes for common queries
    __table_args__ = (
        db.Index('idx_candidate_job', 'candidate_id', 'job_id'),
        db.Index('idx_candidate_status', 'candidate_id', 'status'),
        db.Index('idx_job_score', 'job_id', 'match_score'),
    )
    
    def __repr__(self):
        return f'<Match candidate={self.candidate_id} job={self.job_id} score={self.match_score}>'
