from datetime import datetime, timedelta
import jwt
import os

class AuthService:
    """Handle user authentication and JWT tokens"""
    
    def __init__(self):
        self.secret_key = os.getenv('JWT_SECRET_KEY', 'dev-secret-key-change-in-prod')
        self.algorithm = 'HS256'
        self.token_expiry_hours = 24
    
    def generate_token(self, user_id, email, role='user'):
        """Generate JWT token for user"""
        payload = {
            'user_id': user_id,
            'email': email,
            'role': role,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(hours=self.token_expiry_hours)
        }
        
        try:
            token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
            return token
        except Exception as e:
            return None
    
    def verify_token(self, token):
        """Verify JWT token and return payload"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def hash_password(self, password):
        """Hash password (use bcrypt in production)"""
        # TODO: Implement bcrypt hashing
        return password
    
    def verify_password(self, stored_hash, provided_password):
        """Verify password against hash"""
        # TODO: Implement bcrypt verification
        return stored_hash == provided_password
    
    def refresh_token(self, token):
        """Refresh an existing token"""
        payload = self.verify_token(token)
        if payload:
            return self.generate_token(payload['user_id'], payload['email'], payload.get('role', 'user'))
        return None

auth_service = AuthService()
