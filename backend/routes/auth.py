"""Authentication routes."""
from flask import Blueprint, request, jsonify

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register new user."""
    return jsonify({'message': 'Register endpoint'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user."""
    return jsonify({'message': 'Login endpoint'}), 200

@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    """Refresh token."""
    return jsonify({'message': 'Refresh endpoint'}), 200

@auth_bp.route('/me', methods=['GET'])
def get_profile():
    """Get user profile."""
    return jsonify({'message': 'Profile endpoint'}), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout user."""
    return jsonify({'message': 'Logout endpoint'}), 200
