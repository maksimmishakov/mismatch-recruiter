"""Analytics endpoints."""
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
    days = request.args.get('days', 30, type=int)
   
    try:
        metrics = AnalyticsService.get_dashboard_metrics(days)
        return jsonify({'metrics': metrics}), 200
    except Exception as e:
        logger.error(f"Error fetching dashboard metrics: {e}")
        return jsonify({'error': str(e)}), 500

@bp.route('/funnel', methods=['GET'])
@jwt_required()
def funnel():
    """Get user funnel metrics."""
    days = request.args.get('days', 30, type=int)
   
    try:
        funnel_data = AnalyticsService.get_user_funnel_metrics(days)
        return jsonify({'funnel': funnel_data}), 200
    except Exception as e:
        logger.error(f"Error fetching funnel metrics: {e}")
        return jsonify({'error': str(e)}), 500

@bp.route('/match-quality', methods=['GET'])
@jwt_required()
def match_quality():
    """Get match quality metrics."""
    days = request.args.get('days', 30, type=int)
   
    try:
        quality_data = AnalyticsService.get_match_quality_metrics(days)
        return jsonify({'quality': quality_data}), 200
    except Exception as e:
        logger.error(f"Error fetching quality metrics: {e}")
        return jsonify({'error': str(e)}), 500

@bp.route('/timeline', methods=['GET'])
@jwt_required()
def timeline():
    """Get metrics over time."""
    days = request.args.get('days', 30, type=int)
    interval = request.args.get('interval', 'day')
   
    try:
        timeline_data = AnalyticsService.get_time_series_metrics(days, interval)
        return jsonify({'timeline': timeline_data}), 200
    except Exception as e:
        logger.error(f"Error fetching timeline metrics: {e}")
        return jsonify({'error': str(e)}), 500