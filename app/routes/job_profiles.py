from flask import Blueprint, request, jsonify
from app import db
from app.models import JobProfile

job_profiles_bp = Blueprint('job_profiles', __name__, url_prefix='/api/job-profiles')

@job_profiles_bp.route('/', methods=['POST'])
def create_job_profile():
    data = request.json
    profile = JobProfile(
        job_title=data.get('job_title'),
        required_skills=data.get('required_skills'),
        salary_range=data.get('salary_range'),
        description=data.get('description')
    )
    db.session.add(profile)
    db.session.commit()
    return jsonify(profile.to_dict()), 201

@job_profiles_bp.route('/<int:job_id>', methods=['GET'])
def get_job_profile(job_id):
    profile = JobProfile.query.get(job_id)
    if not profile:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(profile.to_dict()), 200
