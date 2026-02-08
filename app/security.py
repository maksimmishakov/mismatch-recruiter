"""Security utilities and middleware for application hardening."""
import os
import secrets
import hashlib
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app
import logging

logger = logging.getLogger(__name__)


# Security headers middleware
SECURITY_HEADERS = {
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
    'X-XSS-Protection': '1; mode=block',
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
    'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';",
    'Referrer-Policy': 'strict-origin-when-cross-origin',
    'Permissions-Policy': 'geolocation=(), microphone=(), camera=()'
}


def add_security_headers(response):
    """Add security headers to all responses."""
    for header, value in SECURITY_HEADERS.items():
        response.headers[header] = value
    return response


def init_security_middleware(app):
    """Initialize security middleware for Flask app."""
    @app.after_request
    def apply_security_headers(response):
        return add_security_headers(response)
    
    logger.info("Security middleware initialized")
    return app


class SecurityManager:
    """Manage security operations."""
    
    def __init__(self, secret_key=None):
        self.secret_key = secret_key or os.environ.get('SECRET_KEY', self.generate_secret_key())
    
    @staticmethod
    def generate_secret_key(length=64):
        """Generate a secure random secret key."""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def generate_api_key():
        """Generate a secure API key."""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def hash_password(password: str, salt: str = None) -> tuple:
        """Hash password with salt using SHA-256.
        
        Args:
            password: Plain text password
            salt: Optional salt (will be generated if not provided)
            
        Returns:
            Tuple of (hashed_password, salt)
        """
        if salt is None:
            salt = secrets.token_hex(32)
        
        hashed = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        
        return hashed.hex(), salt
    
    @staticmethod
    def verify_password(password: str, hashed_password: str, salt: str) -> bool:
        """Verify password against hash.
        
        Args:
            password: Plain text password to verify
            hashed_password: Stored hashed password
            salt: Salt used for hashing
            
        Returns:
            True if password matches, False otherwise
        """
        new_hash, _ = SecurityManager.hash_password(password, salt)
        return secrets.compare_digest(new_hash, hashed_password)
    
    def generate_jwt_token(self, user_id: int, expiration_hours: int = 24) -> str:
        """Generate JWT authentication token.
        
        Args:
            user_id: User ID to encode in token
            expiration_hours: Token expiration time in hours
            
        Returns:
            JWT token string
        """
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(hours=expiration_hours),
            'iat': datetime.utcnow()
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm='HS256')
        return token
    
    def decode_jwt_token(self, token: str) -> dict:
        """Decode and verify JWT token.
        
        Args:
            token: JWT token to decode
            
        Returns:
            Decoded payload dictionary
            
        Raises:
            jwt.ExpiredSignatureError: If token has expired
            jwt.InvalidTokenError: If token is invalid
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Expired JWT token")
            raise
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid JWT token: {str(e)}")
            raise


# Create global security manager
security_manager = SecurityManager()


def require_auth(f):
    """Decorator to require JWT authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        # Get token from Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]  # Format: "Bearer <token>"
            except IndexError:
                return jsonify({
                    'error': 'Invalid authorization header format',
                    'status': 'error'
                }), 401
        
        if not token:
            return jsonify({
                'error': 'Authentication required',
                'status': 'error'
            }), 401
        
        try:
            payload = security_manager.decode_jwt_token(token)
            request.user_id = payload['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({
                'error': 'Token has expired',
                'status': 'error'
            }), 401
        except jwt.InvalidTokenError:
            return jsonify({
                'error': 'Invalid token',
                'status': 'error'
            }), 401
        
        return f(*args, **kwargs)
    
    return decorated_function


def require_api_key(f):
    """Decorator to require API key authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        
        if not api_key:
            return jsonify({
                'error': 'API key required',
                'status': 'error'
            }), 401
        
        # Verify API key against database or environment
        valid_api_key = os.environ.get('API_KEY')
        
        if not valid_api_key or not secrets.compare_digest(api_key, valid_api_key):
            logger.warning(f"Invalid API key attempted: {api_key[:8]}...")
            return jsonify({
                'error': 'Invalid API key',
                'status': 'error'
            }), 401
        
        return f(*args, **kwargs)
    
    return decorated_function


def sanitize_sql_input(input_str: str) -> str:
    """Sanitize input to prevent SQL injection.
    
    Args:
        input_str: String to sanitize
        
    Returns:
        Sanitized string
    """
    dangerous_chars = ["'", '"', ';', '--', '/*', '*/', 'xp_', 'sp_']
    sanitized = input_str
    
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    
    return sanitized


def check_password_strength(password: str) -> dict:
    """Check password strength and return recommendations.
    
    Args:
        password: Password to check
        
    Returns:
        Dictionary with strength score and recommendations
    """
    score = 0
    recommendations = []
    
    # Check length
    if len(password) >= 8:
        score += 1
    else:
        recommendations.append("Password should be at least 8 characters long")
    
    if len(password) >= 12:
        score += 1
    
    # Check for uppercase
    if any(c.isupper() for c in password):
        score += 1
    else:
        recommendations.append("Add uppercase letters")
    
    # Check for lowercase
    if any(c.islower() for c in password):
        score += 1
    else:
        recommendations.append("Add lowercase letters")
    
    # Check for digits
    if any(c.isdigit() for c in password):
        score += 1
    else:
        recommendations.append("Add numbers")
    
    # Check for special characters
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    if any(c in special_chars for c in password):
        score += 1
    else:
        recommendations.append("Add special characters")
    
    strength_levels = {
        0: 'Very Weak',
        1: 'Weak',
        2: 'Weak',
        3: 'Medium',
        4: 'Strong',
        5: 'Strong',
        6: 'Very Strong'
    }
    
    return {
        'score': score,
        'max_score': 6,
        'strength': strength_levels.get(score, 'Unknown'),
        'recommendations': recommendations,
        'is_strong': score >= 4
    }


def detect_suspicious_activity(request):
    """Detect potentially suspicious request patterns.
    
    Args:
        request: Flask request object
        
    Returns:
        Dictionary with suspicious activity indicators
    """
    suspicious = []
    
    # Check for SQL injection patterns
    sql_patterns = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'DROP', 'UNION', '--', '/*']
    request_data = str(request.get_json() or '') + str(request.args)
    
    for pattern in sql_patterns:
        if pattern in request_data.upper():
            suspicious.append(f"Potential SQL injection: {pattern}")
    
    # Check for XSS patterns
    xss_patterns = ['<script', 'javascript:', 'onerror=', 'onload=']
    for pattern in xss_patterns:
        if pattern.lower() in request_data.lower():
            suspicious.append(f"Potential XSS: {pattern}")
    
    # Check for excessive request rate
    user_agent = request.headers.get('User-Agent', '')
    if not user_agent or user_agent == 'python-requests':
        suspicious.append("Missing or suspicious User-Agent")
    
    return {
        'is_suspicious': len(suspicious) > 0,
        'indicators': suspicious,
        'ip_address': request.remote_addr,
        'user_agent': user_agent
    }


def log_security_event(event_type: str, details: dict):
    """Log security events for audit trail.
    
    Args:
        event_type: Type of security event
        details: Event details dictionary
    """
    logger.warning(f"SECURITY EVENT: {event_type}", extra={
        'extra_data': {
            'event_type': event_type,
            'timestamp': datetime.utcnow().isoformat(),
            **details
        }
    })


if __name__ == '__main__':
    # Generate new secret key
    print(f"New Secret Key: {SecurityManager.generate_secret_key()}")
    
    # Generate new API key
    print(f"New API Key: {SecurityManager.generate_api_key()}")
    
    # Test password hashing
    password = "TestPassword123!"
    hashed, salt = SecurityManager.hash_password(password)
    print(f"Hashed password: {hashed[:32]}...")
    print(f"Verification: {SecurityManager.verify_password(password, hashed, salt)}")
    
    # Test password strength
    strength = check_password_strength(password)
    print(f"Password strength: {strength}")
