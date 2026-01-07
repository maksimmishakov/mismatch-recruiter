"""Authentication decorators for protecting routes."""
from functools import wraps
from flask import request, jsonify, g
from .jwt_handler import jwt_handler

def require_auth(f):
    """Decorator to require valid JWT token."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        # Try to get token from Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'message': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            payload = jwt_handler.validate_token(token)
            g.user_id = payload['user_id']
            g.email = payload['email']
        except Exception as e:
            return jsonify({'message': str(e)}), 401
        
        return f(*args, **kwargs)
    
    return decorated_function

def get_current_user():
    """Get current authenticated user info."""
    return {
        'user_id': g.get('user_id'),
        'email': g.get('email')
    }
