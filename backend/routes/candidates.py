from flask import Blueprint, request, jsonify
from app import db
from backend.models.candidate import Candidate

candidates_bp = Blueprint('candidates', __name__, url_prefix='/api/candidates')

@candidates_bp.route('', methods=['GET'])
def get_candidates():
    candidates = Candidate.query.all()
    return jsonify([c.to_dict() for c in candidates]), 200

@candidates_bp.route('/<int:candidate_id>', methods=['GET'])
def get_candidate(candidate_id):
    candidate = Candidate.query.get_or_404(candidate_id)
    return jsonify(candidate.to_dict()), 200

@candidates_bp.route('', methods=['POST'])
def create_candidate():
    data = request.get_json()
    
    candidate = Candidate(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        phone=data.get('phone'),
        experience_years=data.get('experience_years', 0),
        specialization=data.get('specialization')
    )
    
    if 'skills' in data:
        candidate.set_skills(data['skills'])
    
    db.session.add(candidate)
    db.session.commit()
    
    return jsonify(candidate.to_dict()), 201

@candidates_bp.route('/<int:candidate_id>', methods=['PUT'])
def update_candidate(candidate_id):
    candidate = Candidate.query.get_or_404(candidate_id)
    data = request.get_json()
    
    for key, value in data.items():
        if key == 'skills':
            candidate.set_skills(value)
        elif hasattr(candidate, key):
            setattr(candidate, key, value)
    
    db.session.commit()
    return jsonify(candidate.to_dict()), 200
