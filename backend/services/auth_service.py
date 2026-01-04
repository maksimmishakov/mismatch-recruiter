from datetime import datetime, timedelta
import hashlib

class AuthService:
    """Authentication and Authorization Service"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify_password(password: str, hash_value: str) -> bool:
        """Verify password against hash"""
        return AuthService.hash_password(password) == hash_value
    
    @staticmethod
    def create_token(user_id: int, expires_in=86400) -> dict:
        """Create JWT token"""
        return {
            'user_id': user_id,
            'token': f'token_{user_id}_{datetime.now().timestamp()}',
            'expires_at': (datetime.now() + timedelta(seconds=expires_in)).isoformat()
        }
    
    @staticmethod
    def validate_token(token: str) -> dict:
        """Validate JWT token"""
        if not token or not token.startswith('token_'):
            return {'valid': False, 'error': 'Invalid token'}
        return {'valid': True, 'user_id': int(token.split('_')[1])}
