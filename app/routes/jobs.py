from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Job

jobs_bp = Blueprint('jobs', __name__, url_prefix='/api/jobs')


@jobs_bp.route('', methods=['GET'])
def list_jobs():
    """Get list of all jobs."""
    jobs = Job.query.all()
    return jsonify([j.to_dict() for j in jobs]), 200


@jobs_bp.route('/<int:id>', methods=['GET'])
def get_job(id):
    """Get specific job by ID."""
    job = Job.query.get(id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    return jsonify(job.to_dict()), 200


@jobs_bp.route('', methods=['POST'])
@jwt_required()
def create_job():
    """Create new job."""
    data = request.get_json()
    
    if not data or not data.get('title'):
        return jsonify({'error': 'Title required'}), 400
    
    job = Job(
        title=data['title'],
        description=data.get('description'),
        location=data.get('location'),
        salary_min=data.get('salary_min'),
        salary_max=data.get('salary_max'),
        status=data.get('status', 'ACTIVE')
    )
    
    db.session.add(job)
    db.session.commit()
    return jsonify(job.to_dict()), 201


@jobs_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_job(id):
    """Update job."""
    job = Job.query.get(id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    data = request.get_json()
    if 'title' in data:
        job.title = data['title']
    if 'description' in data:
        job.description = data['description']
    if 'location' in data:
        job.location = data['location']
    if 'salary_min' in data:
        job.salary_min = data['salary_min']
    if 'salary_max' in data:
        job.salary_max = data['salary_max']
    if 'status' in data:
        job.status = data['status']
    
    db.session.commit()
    return jsonify(job.to_dict()), 200


@jobs_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_job(id):
    """Delete job."""
    job = Job.query.get(id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    db.session.delete(job)
    db.session.commit()
    return jsonify({'message': 'Job deleted'}), 204
