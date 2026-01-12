from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, current_app

class User(db.Model):
    """User model for recruiters"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    candidates = db.relationship('Candidate', backref='recruiter', lazy=True)
    jobs = db.relationship('Job', backref='recruiter', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def generate_token(self, expires_in=3600):
        """Generate JWT token"""
        payload = {
            'user_id': self.id,
            'email': self.email,
            'exp': datetime.utcnow().timestamp() + expires_in
        }
        try:
            return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
        except:
            return None
    
    @staticmethod
    def verify_token(token):
        """Verify JWT token"""
        try:
            if not token or not current_app.config.get('SECRET_KEY'):
                return None
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            return User.query.get(payload['user_id'])
        except:
            return None
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'created_at': self.created_at.isoformat()
        }
