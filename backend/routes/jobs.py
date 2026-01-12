from flask import Blueprint, request, jsonify
from app import db
from backend.models.job import Job

jobs_bp = Blueprint('jobs', __name__, url_prefix='/api/jobs')

@jobs_bp.route('', methods=['GET'])
def get_jobs():
    jobs = Job.query.all()
    return jsonify([j.to_dict() for j in jobs]), 200

@jobs_bp.route('/<int:job_id>', methods=['GET'])
def get_job(job_id):
    job = Job.query.get_or_404(job_id)
    return jsonify(job.to_dict()), 200

@jobs_bp.route('', methods=['POST'])
def create_job():
    data = request.get_json()
    
    job = Job(
        title=data['title'],
        description=data['description'],
        company=data['company'],
        location=data['location'],
        salary_min=data.get('salary_min'),
        salary_max=data.get('salary_max'),
        experience_required=data.get('experience_required', 0)
    )
    
    if 'required_skills' in data:
        job.set_required_skills(data['required_skills'])
    
    db.session.add(job)
    db.session.commit()
    
    return jsonify(job.to_dict()), 201

@jobs_bp.route('/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    job = Job.query.get_or_404(job_id)
    data = request.get_json()
    
    for key, value in data.items():
        if key == 'required_skills':
            job.set_required_skills(value)
        elif hasattr(job, key):
            setattr(job, key, value)
    
    db.session.commit()
    return jsonify(job.to_dict()), 200
