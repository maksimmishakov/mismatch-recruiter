---
from flask import Blueprint, request, jsonify
from backend.app import db
from backend.app.models import Match

bp = Blueprint('matches', __name__)

@bp.route('', methods=['GET'])
def list_matches():
    return jsonify([m.to_dict() for m in Match.query.all()]), 200

@bp.route('/<int:id>', methods=['GET'])
def get_match(id):
    m = Match.query.get(id)
    return (jsonify(m.to_dict()), 200) if m else (jsonify({'error': 'Not found'}), 404)

@bp.route('', methods=['POST'])
def create_match():
    data = request.get_json() or {}
    if not data.get('candidate_id') or not data.get('job_id'): return jsonify({'error': 'Missing'}), 400
    m = Match(candidate_id=data['candidate_id'], job_id=data['job_id'],
              match_score=data.get('match_score', 0), status=data.get('status', 'pending'))
    db.session.add(m)
    db.session.commit()
    return jsonify({'message': 'Created', 'match': m.to_dict()}), 201
