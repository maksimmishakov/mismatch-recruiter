from flask import Blueprint, request, jsonify
from app import db
from app.models import Candidate
from flask_jwt_extended import jwt_required, get_jwt_identity

candidates_bp = Blueprint('candidates', __name__, url_prefix='/api/candidates')

@candidates_bp.route('', methods=['GET'])
@jwt_required()
def list_candidates():
    """List all candidates for current user"""
    user_id = get_jwt_identity()
    candidates = Candidate.query.filter_by(user_id=user_id).all()
    return jsonify([c.to_dict() for c in candidates]), 200

@candidates_bp.route('', methods=['POST'])
@jwt_required()
def create_candidate():
    """Create a new candidate"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or not data.get('name') or not data.get('email'):
        return jsonify({'error': 'Missing required fields: name, email'}), 400
    
    try:
        candidate = Candidate(
            user_id=user_id,
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            skills=data.get('skills', []),
            experience_years=data.get('experience_years', 0),
            location=data.get('location'),
            salary_expectation=data.get('salary_expectation')
        )
        db.session.add(candidate)
        db.session.commit()
        
        return jsonify({'id': candidate.id, 'message': 'Candidate created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@candidates_bp.route('/<int:candidate_id>', methods=['GET'])
@jwt_required()
def get_candidate(candidate_id):
    """Get candidate by ID"""
    user_id = get_jwt_identity()
    candidate = Candidate.query.filter_by(id=candidate_id, user_id=user_id).first()
    
    if not candidate:
        return jsonify({'error': 'Candidate not found'}), 404
    return jsonify(candidate.to_dict()), 200

@candidates_bp.route('/<int:candidate_id>', methods=['PUT'])
@jwt_required()
def update_candidate(candidate_id):
    """Update candidate"""
    user_id = get_jwt_identity()
    candidate = Candidate.query.filter_by(id=candidate_id, user_id=user_id).first()
    
    if not candidate:
        return jsonify({'error': 'Candidate not found'}), 404
    
    data = request.get_json()
    try:
        if 'name' in data:
            candidate.name = data['name']
        if 'email' in data:
            candidate.email = data['email']
        if 'skills' in data:
            candidate.skills = data['skills']
        if 'experience_years' in data:
            candidate.experience_years = data['experience_years']
        db.session.commit()
        return jsonify(candidate.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@candidates_bp.route('/<int:candidate_id>', methods=['DELETE'])
@jwt_required()
def delete_candidate(candidate_id):
    """Delete candidate"""
    user_id = get_jwt_identity()
    candidate = Candidate.query.filter_by(id=candidate_id, user_id=user_id).first()
    
    if not candidate:
        return jsonify({'error': 'Candidate not found'}), 404
    
    try:
        db.session.delete(candidate)
        db.session.commit()
        return jsonify({'message': 'Candidate deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
