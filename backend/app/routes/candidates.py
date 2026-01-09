from flask import Blueprint

candidates_bp = Blueprint('candidates', __name__)

@candidates_bp.route('/list', methods=['GET'])
def list_candidates():
    return {'candidates': []}
