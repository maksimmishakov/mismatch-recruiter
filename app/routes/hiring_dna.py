from flask import Blueprint, request, jsonify
from app import db
from app.models import HiringDNA

hiring_dna_bp = Blueprint('hiring_dna', __name__, url_prefix='/api/hiring-dna')

@hiring_dna_bp.route('/', methods=['POST'])
def create_hiring_dna():
    data = request.json
    dna = HiringDNA(
        candidate_id=data.get('candidate_id'),
        dna_profile=data.get('dna_profile'),
        cultural_fit=data.get('cultural_fit'),
        technical_match=data.get('technical_match')
    )
    db.session.add(dna)
    db.session.commit()
    return jsonify(dna.to_dict()), 201

@hiring_dna_bp.route('/<candidate_id>', methods=['GET'])
def get_hiring_dna(candidate_id):
    dna = HiringDNA.query.filter_by(candidate_id=candidate_id).first()
    if not dna:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(dna.to_dict()), 200
