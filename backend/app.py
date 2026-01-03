#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MisMatch Recruiter Backend
Flask application for AI-powered job-candidate matching
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import logging

# Import Blueprints
from app.routes.job_profiles import job_profiles_bp
from app.routes.candidates import candidates_bp
from app.routes.matching_v2 import matching_bp
from app.routes.analytics import analytics_bp
from app.routes.feedback import feedback_bp

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)
    
    # Initialize extensions
    CORS(app, resources={
        r"/api/*": {
            "origins": ["*"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    JWTManager(app)

    # Register Blueprints
    app.register_blueprint(job_profiles_bp)
    app.register_blueprint(candidates_bp)
    app.register_blueprint(matching_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(feedback_bp)
    
    # Routes
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'service': 'MisMatch Recruiter Backend'
        }), 200
    
    @app.route('/api/auth/register', methods=['POST'])
    def register():
        """Register new user"""
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # In production, save to database
        user_id = hash(data['email']) % 10000
        access_token = create_access_token(identity=user_id)
        
        return jsonify({
            'user_id': user_id,
            'email': data['email'],
            'access_token': access_token,
            'created_at': datetime.utcnow().isoformat()
        }), 201
    
    @app.route('/api/auth/login', methods=['POST'])
    def login():
        """User login"""
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Missing credentials'}), 400
        
        # In production, validate against database
        user_id = hash(data['email']) % 10000
        access_token = create_access_token(identity=user_id)
        
        return jsonify({
            'user_id': user_id,
            'email': data['email'],
            'access_token': access_token
        }), 200
    
    @app.route('/api/candidates', methods=['GET'])
    @jwt_required()
    def get_candidates():
        """Get all candidates"""
        current_user = get_jwt_identity()
        
        # Mock data
        candidates = [
            {'id': 1, 'name': 'John Doe', 'position': 'Senior Python Developer', 'skills': ['Python', 'Flask', 'PostgreSQL']},
            {'id': 2, 'name': 'Jane Smith', 'position': 'React Developer', 'skills': ['React', 'TypeScript', 'CSS']},
            {'id': 3, 'name': 'Bob Johnson', 'position': 'Full Stack Developer', 'skills': ['Python', 'React', 'PostgreSQL']}
        ]
        
        return jsonify(candidates), 200
    
    @app.route('/api/jobs', methods=['GET'])
    @jwt_required()
    def get_jobs():
        """Get all job positions"""
        jobs = [
            {'id': 1, 'title': 'Senior Python Developer', 'company': 'TechCorp', 'salary': '$100k-$150k', 'skills': ['Python', 'Flask']},
            {'id': 2, 'title': 'React Developer', 'company': 'WebStudio', 'salary': '$80k-$120k', 'skills': ['React', 'TypeScript']},
            {'id': 3, 'title': 'Full Stack Developer', 'company': 'StartUp Inc', 'salary': '$90k-$130k', 'skills': ['Python', 'React', 'PostgreSQL']}
        ]
        
        return jsonify(jobs), 200
    
    @app.route('/api/matches', methods=['POST'])
    @jwt_required()
    def calculate_match():
        """Calculate match score between candidate and job"""
        data = request.get_json()
        candidate_id = data.get('candidate_id')
        job_id = data.get('job_id')
        
        if not candidate_id or not job_id:
            return jsonify({'error': 'Missing candidate_id or job_id'}), 400
        
        # Mock matching algorithm
        match_score = 85
        
        return jsonify({
            'candidate_id': candidate_id,
            'job_id': job_id,
            'match_score': match_score,
            'recommendation': 'GOOD_MATCH' if match_score >= 75 else 'FAIR_MATCH',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    @app.route('/api/matches/all', methods=['GET'])
    @jwt_required()
    def get_all_matches():
        """Get all matches"""
        matches = [
            {'id': 1, 'candidate_name': 'John Doe', 'position': 'Senior Python Developer', 'match_score': 92, 'recommendation': 'PERFECT_MATCH'},
            {'id': 2, 'candidate_name': 'Jane Smith', 'position': 'React Developer', 'match_score': 88, 'recommendation': 'GOOD_MATCH'},
            {'id': 3, 'candidate_name': 'Bob Johnson', 'position': 'Full Stack Developer', 'match_score': 85, 'recommendation': 'GOOD_MATCH'}
        ]
        
        return jsonify(matches), 200
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return jsonify({'error': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        logger.error(f'Internal error: {error}')
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=False)