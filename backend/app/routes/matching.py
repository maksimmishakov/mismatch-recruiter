from flask import Blueprint

matching_bp = Blueprint('matching', __name__)

@matching_bp.route('/matches', methods=['GET'])
def get_matches():
    return {'matches': []}
