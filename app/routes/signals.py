from flask import Blueprint, request, jsonify
from app import db
from app.models import HiringSignal

signals_bp = Blueprint('signals', __name__, url_prefix='/api/signals')

@signals_bp.route('/', methods=['POST'])
def create_signal():
    data = request.json
    signal = HiringSignal(
        signal_type=data.get('signal_type'),
        signal_value=data.get('signal_value'),
        related_entity=data.get('related_entity')
    )
    db.session.add(signal)
    db.session.commit()
    return jsonify(signal.to_dict()), 201

@signals_bp.route('/<signal_type>', methods=['GET'])
def get_signals_by_type(signal_type):
    signals = HiringSignal.query.filter_by(signal_type=signal_type).all()
    return jsonify([s.to_dict() for s in signals]), 200
