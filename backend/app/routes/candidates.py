from flask import Blueprint, request, jsonify
from backend.app import db
from backend.app.models import Candidate

bp = Blueprint('candidates', __name__)

@bp.route('', methods=['GET'])
def list_candidates():
    return jsonify([c.to_dict() for c in Candidate.query.all()]), 200

@bp.route('/<int:id>', methods=['GET'])
def get_candidate(id):
    c = Candidate.query.get(id)
    return (jsonify(c.to_dict()), 200) if c else (jsonify({'error': 'Not found'}), 404)

@bp.route('', methods=['POST'])
def create_candidate():
    data = request.get_json() or {}
    if not data.get('name') or not data.get('email'): return jsonify({'error': 'Missing'}), 400
    c = Candidate(name=data['name'], email=data['email'], phone=data.get('phone'),
                  skills=data.get('skills'), experience_years=data.get('experience_years', 0))
    db.session.add(c)
    db.session.commit()
    return jsonify({'message': 'Created', 'candidate': c.to_dict()}), 201
