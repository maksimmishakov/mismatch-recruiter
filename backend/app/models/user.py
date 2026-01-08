from ..database import db
from datetime import datetime
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", truncate_error=True)

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    role = db.Column(db.String(20), default='user')  # 'admin', 'recruiter', 'user'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships for cascade delete
    candidates = db.relationship('Candidate', backref='user', lazy=True, cascade='all, delete-orphan')
    jobs = db.relationship('JobPosting', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password: str):
        self.hashed_password = pwd_context.hash(password)
    
    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.hashed_password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'full_name': self.full_name,
            'is_active': self.is_active,
            'role': self.role,
            'created_at': self.created_at.isoformat(),
        }
