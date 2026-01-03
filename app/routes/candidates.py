from flask import Blueprint, request, jsonify
from app.models import Candidate
from app import db

candidates_bp = Blueprint('candidates', __name__)

@candidates_bp.route('/', methods=['POST'])
def create_candidate():
    """Create a new candidate profile"""
    data = request.get_json()
    
    if not data.get('name') or not data.get('email'):
        return jsonify({'error': 'Name and email are required'}), 400
    
    # Check if candidate already exists
    existing = Candidate.query.filter_by(email=data.get('email')).first()
    if existing:
        return jsonify({'error': 'Candidate with this email already exists'}), 400
    
    candidate = Candidate(
        name=data.get('name'),
        email=data.get('email'),
        phone=data.get('phone'),
        resume_text=data.get('resume_text'),
        skills=data.get('skills'),
        experience_years=data.get('experience_years'),
        current_position=data.get('current_position'),
        current_company=data.get('current_company'),
        salary_expectation=data.get('salary_expectation'),
        location=data.get('location'),
        availability=data.get('availability')
    )
    
    db.session.add(candidate)
    db.session.commit()
    
    return jsonify(candidate.to_dict()), 201

@candidates_bp.route('/<int:candidate_id>', methods=['GET'])
def get_candidate(candidate_id):
    """Retrieve a specific candidate by ID"""
    candidate = Candidate.query.get(candidate_id)
    if not candidate:
        return jsonify({'error': 'Candidate not found'}), 404
    
    return jsonify(candidate.to_dict()), 200

@candidates_bp.route('/', methods=['GET'])
def list_candidates():
    """Retrieve all candidates with pagination"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # Query with pagination
    pagination = Candidate.query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    candidates = [candidate.to_dict() for candidate in pagination.items]
    
    return jsonify({
        'data': candidates,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages
        }
    }), 200

@candidates_bp.route('/<int:candidate_id>', methods=['PUT'])
def update_candidate(candidate_id):
    """Update a candidate profile"""
    candidate = Candidate.query.get(candidate_id)
    if not candidate:
        return jsonify({'error': 'Candidate not found'}), 404
    
    data = request.get_json()
    
    # Update fields if provided
    if 'name' in data:
        candidate.name = data['name']
    if 'phone' in data:
        candidate.phone = data['phone']
    if 'resume_text' in data:
        candidate.resume_text = data['resume_text']
    if 'skills' in data:
        candidate.skills = data['skills']
    if 'experience_years' in data:
        candidate.experience_years = data['experience_years']
    if 'current_position' in data:
        candidate.current_position = data['current_position']
    if 'current_company' in data:
        candidate.current_company = data['current_company']
    if 'salary_expectation' in data:
        candidate.salary_expectation = data['salary_expectation']
    if 'location' in data:
        candidate.location = data['location']
    if 'availability' in data:
        candidate.availability = data['availability']
    
    db.session.commit()
    
    return jsonify(candidate.to_dict()), 200

@candidates_bp.route('/<int:candidate_id>', methods=['DELETE'])
def delete_candidate(candidate_id):
    """Delete a candidate profile"""
    candidate = Candidate.query.get(candidate_id)
    if not candidate:
        return jsonify({'error': 'Candidate not found'}), 404
    
    db.session.delete(candidate)
    db.session.commit()
    
    return jsonify({'message': 'Candidate deleted successfully'}), 200