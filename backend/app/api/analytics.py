"""Analytics API endpoints."""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.services.analytics_service import AnalyticsService
import logging

bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')
logger = logging.getLogger(__name__)

@bp.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    """Get dashboard metrics."""
    days = int(request.args.get('days', 30))
    try:
        metrics = AnalyticsService.get_dashboard_metrics(days)
        return jsonify({'metrics': metrics}), 200
    except Exception as e:
        logger.error(f'Error fetching dashboard metrics: {e}')
        return jsonify({'error': str(e)}), 500

@bp.route('/funnel', methods=['GET'])
@jwt_required()
def funnel():
    """Get user funnel metrics."""
    days = int(request.args.get('days', 30))
    try:
        funnel_data = AnalyticsService.get_user_funnel_metrics(days)
        return jsonify({'funnel': funnel_data}), 200
    except Exception as e:
        logger.error(f'Error fetching funnel metrics: {e}')
        return jsonify({'error': str(e)}), 500

@bp.route('/match-quality', methods=['GET'])
@jwt_required()
def match_quality():
    """Get match quality metrics."""
    days = int(request.args.get('days', 30))
    try:
        quality_data = AnalyticsService.get_match_quality_metrics(days)
        return jsonify({'quality': quality_data}), 200
    except Exception as e:
        logger.error(f'Error fetching quality metrics: {e}')
        return jsonify({'error': str(e)}), 500
