from flask import Blueprint, request, jsonify
from app import db
from app.models import Job
from flask_jwt_extended import jwt_required, get_jwt_identity

jobs_bp = Blueprint('jobs', __name__, url_prefix='/api/jobs')

@jobs_bp.route('', methods=['GET'])
@jwt_required()
def list_jobs():
    """List all jobs for current user"""
    user_id = get_jwt_identity()
    jobs = Job.query.filter_by(user_id=user_id).all()
    return jsonify([j.to_dict() for j in jobs]), 200

@jobs_bp.route('', methods=['POST'])
@jwt_required()
def create_job():
    """Create a new job"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or not data.get('title') or not data.get('description'):
        return jsonify({'error': 'Missing required fields: title, description'}), 400
    
    try:
        job = Job(
            user_id=user_id,
            title=data.get('title'),
            description=data.get('description'),
            required_skills=data.get('required_skills', []),
            min_experience=data.get('min_experience', 0),
            min_salary=data.get('min_salary'),
            max_salary=data.get('max_salary'),
            location=data.get('location'),
            employment_type=data.get('employment_type', 'FULL_TIME'),
            status=data.get('status', 'OPEN')
        )
        db.session.add(job)
        db.session.commit()
        return jsonify({'id': job.id, 'message': 'Job created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@jobs_bp.route('/<int:job_id>', methods=['GET'])
@jwt_required()
def get_job(job_id):
    """Get job by ID"""
    user_id = get_jwt_identity()
    job = Job.query.filter_by(id=job_id, user_id=user_id).first()
    
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    return jsonify(job.to_dict()), 200

@jobs_bp.route('/<int:job_id>', methods=['PUT'])
@jwt_required()
def update_job(job_id):
    """Update job"""
    user_id = get_jwt_identity()
    job = Job.query.filter_by(id=job_id, user_id=user_id).first()
    
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    data = request.get_json()
    try:
        if 'title' in data:
            job.title = data['title']
        if 'description' in data:
            job.description = data['description']
        if 'required_skills' in data:
            job.required_skills = data['required_skills']
        if 'status' in data:
            job.status = data['status']
        db.session.commit()
        return jsonify(job.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@jobs_bp.route('/<int:job_id>', methods=['DELETE'])
@jwt_required()
def delete_job(job_id):
    """Delete job"""
    user_id = get_jwt_identity()
    job = Job.query.filter_by(id=job_id, user_id=user_id).first()
    
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    try:
        db.session.delete(job)
        db.session.commit()
        return jsonify({'message': 'Job deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
