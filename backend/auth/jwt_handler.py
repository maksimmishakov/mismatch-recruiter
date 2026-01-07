"""JWT token handler for authentication."""
import jwt
import os
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app

class JWTHandler:
    """Handles JWT token generation and validation."""
    
    def __init__(self, secret_key=None):
        self.secret_key = secret_key or os.getenv('JWT_SECRET_KEY', 'your-secret-key')
        self.algorithm = 'HS256'
        self.expiration_hours = int(os.getenv('JWT_EXPIRATION_HOURS', 24))
    
    def generate_token(self, user_id, email, expires_in=None):
        """Generate JWT token for user."""
        if expires_in is None:
            expires_in = self.expiration_hours
        
        payload = {
            'user_id': user_id,
            'email': email,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(hours=expires_in)
        }
        
        try:
            token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
            return token
        except Exception as e:
            raise Exception(f"Error generating token: {str(e)}")
    
    def validate_token(self, token):
        """Validate JWT token and return payload."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise Exception("Token has expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid token")
    
    def refresh_token(self, token):
        """Generate a new token using existing token payload."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm], options={"verify_exp": False})
            user_id = payload.get('user_id')
            email = payload.get('email')
            return self.generate_token(user_id, email)
        except Exception as e:
            raise Exception(f"Error refreshing token: {str(e)}")

# Global JWT handler instance
jwt_handler = JWTHandler()
