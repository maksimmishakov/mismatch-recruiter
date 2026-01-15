"""Candidates API routes for MisMatch Recruiter"""
from flask import Blueprint, request, jsonify
from app import db
from app.models import Candidate, User
from sqlalchemy.exc import IntegrityError
import logging

logger = logging.getLogger(__name__)

blueprint = Blueprint('candidates', __name__, url_prefix='/api/candidates')

@blueprint.route('', methods=['GET'])
def get_candidates():
    """Get all candidates for the current user."""
    try:
        candidates = Candidate.query.all()
        return jsonify([c.to_dict() for c in candidates]), 200
    except Exception as e:
        logger.error(f'Error getting candidates: {e}')
        return jsonify({'error': 'Internal server error'}), 500

@blueprint.route('', methods=['POST'])
def create_candidate():
    """Create a new candidate."""
    try:
        # Validate JSON content
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Validate required fields
        required_fields = ['first_name', 'last_name', 'email']
        missing_fields = [f for f in required_fields if f not in data]
        if missing_fields:
            return jsonify({'error': f'Missing required fields: {missing_fields}'}), 422
        
        # Create candidate
        candidate = Candidate(
            user_id=1,  # Default for testing
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=data.get('email'),
            phone=data.get('phone'),
            location=data.get('location'),
            skills=data.get('skills'),
            experience_years=data.get('experience_years'),
            summary=data.get('summary')
        )
        
        db.session.add(candidate)
        db.session.commit()
        
        return jsonify(candidate.to_dict()), 201
    
    except ValueError as e:
        logger.error(f'Validation error creating candidate: {e}')
        return jsonify({'error': str(e)}), 422
    except IntegrityError as e:
        db.session.rollback()
        logger.error(f'Database integrity error creating candidate: {e}')
        return jsonify({'error': 'Duplicate entry or data constraint violation'}), 422
    except Exception as e:
        db.session.rollback()
        logger.error(f'Error creating candidate: {e}')
        return jsonify({'error': 'Internal server error'}), 500

@blueprint.route('/<int:candidate_id>', methods=['GET'])
def get_candidate(candidate_id):
    """Get a specific candidate."""
    try:
        candidate = Candidate.query.get(candidate_id)
        if not candidate:
            return jsonify({'error': 'Candidate not found'}), 404
        return jsonify(candidate.to_dict()), 200
    except Exception as e:
        logger.error(f'Error getting candidate {candidate_id}: {e}')
        return jsonify({'error': 'Internal server error'}), 500

@blueprint.route('/<int:candidate_id>', methods=['PUT'])
def update_candidate(candidate_id):
    """Update a candidate."""
    try:
        if not request.is_json:
            return jsonify({'error': 'Request must be JSON'}), 400
        
        candidate = Candidate.query.get(candidate_id)
        if not candidate:
            return jsonify({'error': 'Candidate not found'}), 404
        
        data = request.get_json()
        candidate.first_name = data.get('first_name', candidate.first_name)
        candidate.last_name = data.get('last_name', candidate.last_name)
        candidate.email = data.get('email', candidate.email)
        candidate.phone = data.get('phone', candidate.phone)
        candidate.location = data.get('location', candidate.location)
        candidate.skills = data.get('skills', candidate.skills)
        candidate.experience_years = data.get('experience_years', candidate.experience_years)
        candidate.summary = data.get('summary', candidate.summary)
        
        db.session.commit()
        return jsonify(candidate.to_dict()), 200
    
    except Exception as e:
        db.session.rollback()
        logger.error(f'Error updating candidate {candidate_id}: {e}')
        return jsonify({'error': 'Internal server error'}), 500

@blueprint.route('/<int:candidate_id>', methods=['DELETE'])
def delete_candidate(candidate_id):
    """Delete a candidate."""
    try:
        candidate = Candidate.query.get(candidate_id)
        if not candidate:
            return jsonify({'error': 'Candidate not found'}), 404
        
        db.session.delete(candidate)
        db.session.commit()
        return jsonify({'message': 'Candidate deleted'}), 200
    
    except Exception as e:
        db.session.rollback()
        logger.error(f'Error deleting candidate {candidate_id}: {e}')
        return jsonify({'error': 'Internal server error'}), 500
