# Jobs CRUD routes
from flask import Blueprint, request, jsonify
from app.models import db, Job
import logging

logger = logging.getLogger(__name__)

jobs_bp = Blueprint('jobs', __name__, url_prefix='/api/jobs')


@jobs_bp.route('', methods=['GET'])
def list_jobs():
    """Get all jobs."""
    try:
        jobs = Job.query.all()
        return jsonify([
            {
                'id': j.id,
                'title': j.title,
                'description': j.description,
                'company': j.company,
                'status': j.status,
                'created_at': j.created_at.isoformat() if j.created_at else None
            }
            for j in jobs
        ]), 200
    except Exception as e:
        logger.error(f'Error listing jobs: {e}')
        return jsonify({'error': 'Failed to list jobs'}), 500


@jobs_bp.route('/<int:job_id>', methods=['GET'])
def get_job(job_id):
    """Get a specific job."""
    try:
        job = Job.query.get(job_id)
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        return jsonify({
            'id': job.id,
            'title': job.title,
            'description': job.description,
            'company': job.company,
            'status': job.status,
            'created_at': job.created_at.isoformat() if job.created_at else None
        }), 200
    except Exception as e:
        logger.error(f'Error getting job {job_id}: {e}')
        return jsonify({'error': 'Failed to get job'}), 500


@jobs_bp.route('', methods=['POST'])
def create_job():
    """Create a new job."""
    try:
        data = request.get_json()
        
        if not data or not data.get('title') or not data.get('company'):
            return jsonify({'error': 'Missing required fields'}), 400
        
        job = Job(
            title=data['title'],
            description=data.get('description', ''),
            company=data['company'],
            status=data.get('status', 'open')
        )
        
        db.session.add(job)
        db.session.commit()
        
        logger.info(f'Job created: {job.title}')
        
        return jsonify({
            'id': job.id,
            'title': job.title,
            'description': job.description,
            'company': job.company,
            'status': job.status,
            'created_at': job.created_at.isoformat() if job.created_at else None
        }), 201
    except Exception as e:
        logger.error(f'Error creating job: {e}')
        db.session.rollback()
        return jsonify({'error': 'Failed to create job'}), 500


@jobs_bp.route('/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    """Update a job."""
    try:
        job = Job.query.get(job_id)
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        data = request.get_json()
        
        if 'title' in data:
            job.title = data['title']
        if 'description' in data:
            job.description = data['description']
        if 'company' in data:
            job.company = data['company']
        if 'status' in data:
            job.status = data['status']
        
        db.session.commit()
        
        logger.info(f'Job updated: {job.id}')
        
        return jsonify({
            'id': job.id,
            'title': job.title,
            'description': job.description,
            'company': job.company,
            'status': job.status,
            'created_at': job.created_at.isoformat() if job.created_at else None
        }), 200
    except Exception as e:
        logger.error(f'Error updating job {job_id}: {e}')
        db.session.rollback()
        return jsonify({'error': 'Failed to update job'}), 500


@jobs_bp.route('/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    """Delete a job."""
    try:
        job = Job.query.get(job_id)
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        db.session.delete(job)
        db.session.commit()
        
        logger.info(f'Job deleted: {job_id}')
        
        return jsonify({'message': 'Job deleted'}), 200
    except Exception as e:
        logger.error(f'Error deleting job {job_id}: {e}')
        db.session.rollback()
        return jsonify({'error': 'Failed to delete job'}), 500
