# Authentication routes with proper error handling
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User
import logging

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


def is_valid_email(email):
    """Validate email format."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def is_strong_password(password):
    """Validate password strength."""
    return len(password) >= 8


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    try:
        data = request.get_json()
        
        # Validate input
        if not data or not data.get('username') or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Missing required fields'}), 400
        
        if not is_valid_email(data['email']):
            return jsonify({'error': 'Invalid email format'}), 400
        
        if not is_strong_password(data['password']):
            return jsonify({'error': 'Password too weak'}), 400
        
        # Check if email already exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({'error': 'Email already registered'}), 409
        
        # Create new user
        user = User(
            username=data['username'],
            email=data['email'],
            password_hash=generate_password_hash(data['password']),
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', '')
        )
        user.is_active = True
        
        db.session.add(user)
        db.session.commit()
        
        logger.info(f'User registered: {user.email}')
        
        return jsonify({
            'user_id': user.id,
            'id': user.id,
            'username': user.username,
            'email': user.email
        }), 201
        
    except Exception as e:
        logger.error(f'Registration error: {e}')
        return jsonify({'error': 'Registration failed'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login a user."""
    try:
        data = request.get_json()
        
        # Validate input
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Missing email or password'}), 400
        
        # Find user
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not check_password_hash(user.password_hash, data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'User account is disabled'}), 403
        
        try:
            from app.utils import create_access_token, create_refresh_token
            token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)
        except ImportError:
            logger.warning('JWT utilities not found, using simple token')
            token = f'token_{user.id}_{user.email}'
            refresh_token = f'refresh_token_{user.id}_{user.email}'
        
        logger.info(f'User logged in: {user.email}')
        
        return jsonify({
            'access_token': token,
            'refresh_token': refresh_token,
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role.value,
        }), 200
        
    except Exception as e:
        logger.error(f'Login error: {e}')
        return jsonify({'error': 'Login failed'}), 500


@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    """Get current user information."""
    try:
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'Missing authorization header'}), 401
        
        # Extract token
        try:
            scheme, token = auth_header.split()
            if scheme.lower() != 'bearer':
                return jsonify({'error': 'Invalid authorization scheme'}), 401
        except ValueError:
            return jsonify({'error': 'Invalid authorization header'}), 401
        
        # Parse token to get user ID
        try:
            from app.utils import decode_token
            user_id = decode_token(token)
        except ImportError:
            logger.warning('JWT utilities not found, parsing simple token')
            parts = token.split('_')
            if len(parts) < 2:
                return jsonify({'error': 'Invalid token'}), 401
            user_id = int(parts[1])
        except Exception as e:
            logger.error(f'Token decode error: {e}')
            return jsonify({'error': 'Invalid token'}), 401
        
        # Get user from database
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if not user.is_active:
            return jsonify({'error': 'User account is disabled'}), 403
        
        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role.value,
        }), 200
        
    except Exception as e:
        logger.error(f'Get current user error: {e}')
        return jsonify({'error': 'Failed to get user information'}), 500
