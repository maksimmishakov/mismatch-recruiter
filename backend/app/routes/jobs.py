from flask import Blueprint, request, jsonify
from backend.app import db
from backend.app.models import Job

bp = Blueprint('jobs', __name__)

@bp.route('', methods=['GET'])
def list_jobs():
    return jsonify([j.to_dict() for j in Job.query.all()]), 200

@bp.route('/<int:id>', methods=['GET'])
def get_job(id):
    j = Job.query.get(id)
    return (jsonify(j.to_dict()), 200) if j else (jsonify({'error': 'Not found'}), 404)

@bp.route('', methods=['POST'])
def create_job():
    data = request.get_json() or {}
    if not data.get('title'): return jsonify({'error': 'Missing'}), 400
    j = Job(title=data['title'], description=data.get('description'),
            required_skills=data.get('required_skills'), company=data.get('company'))
    db.session.add(j)
    db.session.commit()
    return jsonify({'message': 'Created', 'job': j.to_dict()}), 201
