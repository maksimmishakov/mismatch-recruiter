from flask import Blueprint, request, jsonify
from app import db
from backend.models.match import Match

matches_bp = Blueprint('matches', __name__, url_prefix='/api/matches')

@matches_bp.route('', methods=['GET'])
def get_matches():
    matches = Match.query.all()
    return jsonify([m.to_dict() for m in matches]), 200

@matches_bp.route('/<int:match_id>', methods=['GET'])
def get_match(match_id):
    match = Match.query.get_or_404(match_id)
    return jsonify(match.to_dict()), 200

@matches_bp.route('', methods=['POST'])
def create_match():
    data = request.get_json()
    
    match = Match(
        candidate_id=data['candidate_id'],
        job_id=data['job_id'],
        match_score=data.get('match_score', 0.0),
        status=data.get('status', 'pending')
    )
    
    db.session.add(match)
    db.session.commit()
    
    return jsonify(match.to_dict()), 201

@matches_bp.route('/<int:match_id>', methods=['PUT'])
def update_match(match_id):
    match = Match.query.get_or_404(match_id)
    data = request.get_json()
    
    for key, value in data.items():
        if hasattr(match, key):
            setattr(match, key, value)
    
    db.session.commit()
    return jsonify(match.to_dict()), 200
