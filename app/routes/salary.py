from flask import Blueprint, request, jsonify
from app import db
from app.models import SalaryData

salary_bp = Blueprint('salary', __name__, url_prefix='/api/salary')

@salary_bp.route('/', methods=['POST'])
def create_salary_data():
    data = request.json
    salary = SalaryData(
        position=data.get('position'),
        base_salary=data.get('base_salary'),
        bonus_percentage=data.get('bonus_percentage'),
        benefits=data.get('benefits'),
        market_rate=data.get('market_rate')
    )
    db.session.add(salary)
    db.session.commit()
    return jsonify(salary.to_dict()), 201

@salary_bp.route('/optimize-offer', methods=['POST'])
def optimize_offer():
    data = request.json
    base_salary = float(data.get('base_salary', 0))
    market_rate = float(data.get('market_rate', 0))
    optimal_salary = (base_salary + market_rate) / 2
    return jsonify({
        'base_salary': base_salary,
        'market_rate': market_rate,
        'optimal_salary': optimal_salary
    }), 200
