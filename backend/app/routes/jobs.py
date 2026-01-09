from flask import Blueprint

jobs_bp = Blueprint('jobs', __name__)

@jobs_bp.route('/list', methods=['GET'])
def list_jobs():
    return {'jobs': []}
