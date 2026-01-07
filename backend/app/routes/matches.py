from flask import Blueprint, request, jsonify
from app import db
from app.models import Match, Candidate, Job
from flask_jwt_extended import jwt_required, get_jwt_identity

matches_bp = Blueprint('matches', __name__, url_prefix='/api/matches')

@matches_bp.route('', methods=['GET'])
@jwt_required()
def list_matches():
    """List all matches for current user's jobs"""
    user_id = get_jwt_identity()
    user_jobs = Job.query.filter_by(user_id=user_id).with_entities(Job.id).all()
    job_ids = [j[0] for j in user_jobs]
    
    matches = Match.query.filter(Match.job_id.in_(job_ids)).all()
    return jsonify([m.to_dict() for m in matches]), 200

@matches_bp.route('', methods=['POST'])
@jwt_required()
def create_match():
    """Create a new match"""
    data = request.get_json()
    
    if not data or not data.get('candidate_id') or not data.get('job_id'):
        return jsonify({'error': 'Missing required fields: candidate_id, job_id'}), 400
    
    try:
        match = Match(
            candidate_id=data.get('candidate_id'),
            job_id=data.get('job_id'),
            score=data.get('score', 0.0),
            skill_match=data.get('skill_match', 0.0),
            experience_match=data.get('experience_match', 0.0),
            salary_match=data.get('salary_match', 0.0),
            status=data.get('status', 'NEW'),
            notes=data.get('notes')
        )
        db.session.add(match)
        db.session.commit()
        return jsonify({'id': match.id, 'message': 'Match created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@matches_bp.route('/<int:match_id>', methods=['GET'])
@jwt_required()
def get_match(match_id):
    """Get match by ID"""
    match = Match.query.get(match_id)
    
    if not match:
        return jsonify({'error': 'Match not found'}), 404
    return jsonify(match.to_dict()), 200

@matches_bp.route('/<int:match_id>', methods=['PUT'])
@jwt_required()
def update_match(match_id):
    """Update match"""
    match = Match.query.get(match_id)
    
    if not match:
        return jsonify({'error': 'Match not found'}), 404
    
    data = request.get_json()
    try:
        if 'score' in data:
            match.score = data['score']
        if 'status' in data:
            match.status = data['status']
        if 'notes' in data:
            match.notes = data['notes']
        db.session.commit()
        return jsonify(match.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@matches_bp.route('/<int:match_id>', methods=['DELETE'])
@jwt_required()
def delete_match(match_id):
    """Delete match"""
    match = Match.query.get(match_id)
    
    if not match:
        return jsonify({'error': 'Match not found'}), 404
    
    try:
        db.session.delete(match)
        db.session.commit()
        return jsonify({'message': 'Match deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
