from flask import Blueprint, request, jsonify
from backend.services.job_service import JobService
from backend.services.salary_service import SalaryService
from backend.services.match_service import MatchService
from backend.services.analytics_service import AnalyticsService

api = Blueprint('api', __name__, url_prefix='/api')

# Job Endpoints
@api.route('/jobs', methods=['POST'])
def create_job():
    data = request.get_json()
    return jsonify(JobService.create_job(1, data))

@api.route('/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    return jsonify(JobService.get_job(job_id))

@api.route('/jobs', methods=['GET'])
def list_jobs():
    return jsonify(JobService.list_jobs(1))

@api.route('/jobs/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    data = request.get_json()
    return jsonify(JobService.update_job(job_id, data))

@api.route('/jobs/<int:job_id>/close', methods=['POST'])
def close_job(job_id):
    return jsonify(JobService.close_job(job_id))

# Salary Endpoints
@api.route('/salary/range', methods=['GET'])
def get_salary_range():
    title = request.args.get('title', 'Developer')
    seniority = request.args.get('seniority', 'Mid')
    location = request.args.get('location', 'USA')
    return jsonify(SalaryService.get_salary_range(title, seniority, location))

@api.route('/salary/match', methods=['POST'])
def salary_match():
    data = request.get_json()
    return jsonify(SalaryService.calculate_salary_match(
        data['job_min'], data['job_max'],
        data['candidate_min'], data['candidate_max']
    ))

# Match Endpoints
@api.route('/matches', methods=['POST'])
def create_match():
    data = request.get_json()
    return jsonify(MatchService.create_match(
        data['candidate_id'], data['job_id'],
        data.get('candidate', {}), data.get('job', {})
    ))

@api.route('/matches/<int:job_id>', methods=['GET'])
def get_matches(job_id):
    return jsonify({'matches': []})

# Analytics Endpoints
@api.route('/analytics/dashboard', methods=['GET'])
def dashboard_stats():
    return jsonify(AnalyticsService.get_dashboard_stats(1))

@api.route('/analytics/job/<int:job_id>', methods=['GET'])
def job_performance(job_id):
    return jsonify(AnalyticsService.get_job_performance(job_id))

@api.route('/analytics/trends', methods=['GET'])
def market_trends():
    location = request.args.get('location', 'USA')
    return jsonify(AnalyticsService.get_market_trends(location))

@api.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'mismatch-recruiter'})
