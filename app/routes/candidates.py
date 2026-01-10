from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Candidate

candidates_bp = Blueprint('candidates', __name__, url_prefix='/api/candidates')


@candidates_bp.route('', methods=['GET'])
def list_candidates():
    """Get list of all candidates."""
    candidates = Candidate.query.all()
    return jsonify([c.to_dict() for c in candidates]), 200


@candidates_bp.route('/<int:id>', methods=['GET'])
def get_candidate(id):
    """Get specific candidate by ID."""
    candidate = Candidate.query.get(id)
    if not candidate:
        return jsonify({'error': 'Candidate not found'}), 404
    return jsonify(candidate.to_dict()), 200


@candidates_bp.route('', methods=['POST'])
@jwt_required()
def create_candidate():
    """Create new candidate."""
    data = request.get_json()
    
    if not data or not data.get('first_name') or not data.get('last_name'):
        return jsonify({'error': 'First name and last name required'}), 400
    
    candidate = Candidate(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data.get('email'),
        phone=data.get('phone'),
        status=data.get('status', 'ACTIVE')
    )
    
    db.session.add(candidate)
    db.session.commit()
    return jsonify(candidate.to_dict()), 201


@candidates_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_candidate(id):
    """Update candidate."""
    candidate = Candidate.query.get(id)
    if not candidate:
        return jsonify({'error': 'Candidate not found'}), 404
    
    data = request.get_json()
    if 'first_name' in data:
        candidate.first_name = data['first_name']
    if 'last_name' in data:
        candidate.last_name = data['last_name']
    if 'email' in data:
        candidate.email = data['email']
    if 'phone' in data:
        candidate.phone = data['phone']
    if 'status' in data:
        candidate.status = data['status']
    
    db.session.commit()
    return jsonify(candidate.to_dict()), 200


@candidates_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_candidate(id):
    """Delete candidate."""
    candidate = Candidate.query.get(id)
    if not candidate:
        return jsonify({'error': 'Candidate not found'}), 404
    
    db.session.delete(candidate)
    db.session.commit()
    return jsonify({'message': 'Candidate deleted'}), 204
