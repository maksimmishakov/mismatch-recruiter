# Authentication routes with proper error handling
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User
import logging

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register new user."""
    try:
        data = request.get_json()
        
        # Validate input
        if not data or not data.get('username') or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Missing required fields: username, email, password'}), 400
        
        # Check if email already exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({'error': 'Email already registered'}), 409
        
        # Create new user
        try:
            user = User(
                username=data['username'],
                email=data['email'],
                password_hash=generate_password_hash(data['password']),
                role='RECRUITER',  # Default role
                is_active=True,
            )
            db.session.add(user)
            db.session.commit()
            logger.info(f'New user registered: {user.email}')
            
            return jsonify({
                'message': 'User created successfully',
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role.value,
            }), 201
        except Exception as e:
            db.session.rollback()
            logger.error(f'Error creating user: {e}')
            return jsonify({'error': f'Failed to create user: {str(e)}'}), 500
    except Exception as e:
        logger.error(f'Registration error: {e}')
        return jsonify({'error': 'Registration failed'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user and return JWT tokens."""
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Missing email or password'}), 400
        
        # Find user
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not check_password_hash(user.password_hash, data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'User account is disabled'}), 403
        
        try:
            # Create simplified token (for now, just return user ID as token)
            # In production, use Flask-JWT-Extended
            token = f'token_{user.id}_{user.email}'
            logger.info(f'User logged in: {user.email}')
            
            return jsonify({
                'access_token': token,
                'refresh_token': token,
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role.value,
            }), 200
        except Exception as e:
            logger.error(f'Token creation error: {e}')
            return jsonify({'error': 'Failed to create tokens'}), 500
    except Exception as e:
        logger.error(f'Login error: {e}')
        return jsonify({'error': 'Login failed'}), 500
