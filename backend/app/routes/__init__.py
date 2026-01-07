"""Application routes"""
from flask import Blueprint, jsonify

def create_routes(app):
    """Create and register all routes"""
    
    # Health check
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({'status': 'ok', 'message': 'Server is running'}), 200
    
    # Auth routes
    @app.route('/api/auth/login', methods=['POST'])
    def login():
        return jsonify({'message': 'Login endpoint'}), 200
    
    @app.route('/api/auth/register', methods=['POST'])
    def register():
        return jsonify({'message': 'Register endpoint'}), 200
    
    # Candidates routes
    @app.route('/api/candidates', methods=['GET'])
    def get_candidates():
        return jsonify({'candidates': []}), 200
    
    @app.route('/api/candidates/<int:candidate_id>', methods=['GET'])
    def get_candidate(candidate_id):
        return jsonify({'candidate_id': candidate_id}), 200
    
    @app.route('/api/candidates', methods=['POST'])
    def create_candidate():
        return jsonify({'message': 'Candidate created'}), 201
    
    # Jobs routes
    @app.route('/api/jobs', methods=['GET'])
    def get_jobs():
        return jsonify({'jobs': []}), 200
    
    @app.route('/api/jobs/<int:job_id>', methods=['GET'])
    def get_job(job_id):
        return jsonify({'job_id': job_id}), 200
    
    @app.route('/api/jobs', methods=['POST'])
    def create_job():
        return jsonify({'message': 'Job created'}), 201
    
    # Matches routes
    @app.route('/api/matches', methods=['GET'])
    def get_matches():
        return jsonify({'matches': []}), 200
