# Candidates CRUD routes
from flask import Blueprint, request, jsonify
from app.models import db, Candidate, User
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

candidates_bp = Blueprint('candidates', __name__, url_prefix='/api/candidates')


@candidates_bp.route('', methods=['GET'])
def list_candidates():
    """Get all candidates."""
    try:
        candidates = Candidate.query.all()
        return jsonify([
            {
                'id': c.id,
                'full_name': c.full_name,
                'email': c.email,
                'phone': c.phone,
                'status': c.status,
                'created_at': c.created_at.isoformat() if c.created_at else None
            }
            for c in candidates
        ]), 200
    except Exception as e:
        logger.error(f'Error listing candidates: {e}')
        return jsonify({'error': 'Failed to list candidates'}), 500


@candidates_bp.route('/<int:candidate_id>', methods=['GET'])
def get_candidate(candidate_id):
    """Get a specific candidate."""
    try:
        candidate = Candidate.query.get(candidate_id)
        if not candidate:
            return jsonify({'error': 'Candidate not found'}), 404
        
        return jsonify({
            'id': candidate.id,
            'full_name': candidate.full_name,
            'email': candidate.email,
            'phone': candidate.phone,
            'status': candidate.status,
            'created_at': candidate.created_at.isoformat() if candidate.created_at else None
        }), 200
    except Exception as e:
        logger.error(f'Error getting candidate {candidate_id}: {e}')
        return jsonify({'error': 'Failed to get candidate'}), 500


@candidates_bp.route('', methods=['POST'])
def create_candidate():
    """Create a new candidate."""
    try:
        data = request.get_json()
        
        if not data or not data.get('full_name') or not data.get('email'):
            return jsonify({'error': 'Missing required fields'}), 400
        
        candidate = Candidate(
            full_name=data['full_name'],
            email=data['email'],
            phone=data.get('phone', ''),
            status=data.get('status', 'new')
        )
        
        db.session.add(candidate)
        db.session.commit()
        
        logger.info(f'Candidate created: {candidate.full_name}')
        
        return jsonify({
            'id': candidate.id,
            'full_name': candidate.full_name,
            'email': candidate.email,
            'phone': candidate.phone,
            'status': candidate.status,
            'created_at': candidate.created_at.isoformat() if candidate.created_at else None
        }), 201
    except Exception as e:
        logger.error(f'Error creating candidate: {e}')
        db.session.rollback()
        return jsonify({'error': 'Failed to create candidate'}), 500


@candidates_bp.route('/<int:candidate_id>', methods=['PUT'])
def update_candidate(candidate_id):
    """Update a candidate."""
    try:
        candidate = Candidate.query.get(candidate_id)
        if not candidate:
            return jsonify({'error': 'Candidate not found'}), 404
        
        data = request.get_json()
        
        if 'full_name' in data:
            candidate.full_name = data['full_name']
        if 'email' in data:
            candidate.email = data['email']
        if 'phone' in data:
            candidate.phone = data['phone']
        if 'status' in data:
            candidate.status = data['status']
        
        db.session.commit()
        
        logger.info(f'Candidate updated: {candidate.id}')
        
        return jsonify({
            'id': candidate.id,
            'full_name': candidate.full_name,
            'email': candidate.email,
            'phone': candidate.phone,
            'status': candidate.status,
            'created_at': candidate.created_at.isoformat() if candidate.created_at else None
        }), 200
    except Exception as e:
        logger.error(f'Error updating candidate {candidate_id}: {e}')
        db.session.rollback()
        return jsonify({'error': 'Failed to update candidate'}), 500


@candidates_bp.route('/<int:candidate_id>', methods=['DELETE'])
def delete_candidate(candidate_id):
    """Delete a candidate."""
    try:
        candidate = Candidate.query.get(candidate_id)
        if not candidate:
            return jsonify({'error': 'Candidate not found'}), 404
        
        db.session.delete(candidate)
        db.session.commit()
        
        logger.info(f'Candidate deleted: {candidate_id}')
        
        return jsonify({'message': 'Candidate deleted'}), 200
    except Exception as e:
        logger.error(f'Error deleting candidate {candidate_id}: {e}')
        db.session.rollback()
        return jsonify({'error': 'Failed to delete candidate'}), 500
