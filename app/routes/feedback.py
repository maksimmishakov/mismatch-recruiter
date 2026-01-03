from flask import Blueprint, request, jsonify
from app.models import Feedback, FeatureRequest
from app.services.feedback_service import FeedbackService, FeedbackType
from app import db
from datetime import datetime

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/', methods=['POST'])
def submit_feedback():
    """Submit user feedback with rating and optional comment"""
    data = request.get_json()
    
    if not data.get('rating'):
        return jsonify({'error': 'Rating is required'}), 400
    
    try:
        feedback_type = FeedbackType(data.get('feedback_type', 'general'))
    except ValueError:
        feedback_type = FeedbackType.GENERAL
    
    result = FeedbackService.collect_feedback(
        user_id=data.get('user_id'),
        rating=int(data.get('rating')),
        comment=data.get('comment'),
        feedback_type=feedback_type,
        email=data.get('email')
    )
    
    return jsonify(result), 201

@feedback_bp.route('/feature-request', methods=['POST'])
def submit_feature_request():
    """Submit a feature request"""
    data = request.get_json()
    
    if not data.get('feature_name'):
        return jsonify({'error': 'Feature name is required'}), 400
    
    result = FeedbackService.record_feature_request(
        user_id=data.get('user_id'),
        feature_name=data.get('feature_name'),
        description=data.get('description'),
        priority=data.get('priority', 3)
    )
    
    return jsonify(result), 201

@feedback_bp.route('/summary/daily', methods=['GET'])
def get_daily_summary():
    """Get daily feedback summary"""
    summary = FeedbackService.get_daily_feedback_summary()
    return jsonify(summary), 200

@feedback_bp.route('/summary/weekly', methods=['GET'])
def get_weekly_summary():
    """Get weekly feedback summary"""
    summary = FeedbackService.get_weekly_feedback_summary()
    return jsonify(summary), 200

@feedback_bp.route('/features/top', methods=['GET'])
def get_top_features():
    """Get top requested features"""
    summary = FeedbackService.get_feature_requests_summary()
    return jsonify(summary), 200

@feedback_bp.route('/list', methods=['GET'])
def list_feedback():
    """List all feedback with pagination"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    days = request.args.get('days', 7, type=int)  # Last N days
    
    from datetime import timedelta
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    feedback_list = Feedback.query.filter(
        Feedback.created_at >= cutoff_date
    ).order_by(
        Feedback.created_at.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'data': [f.to_dict() for f in feedback_list.items],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': feedback_list.total,
            'pages': feedback_list.pages
        }
    }), 200

@feedback_bp.route('/features/list', methods=['GET'])
def list_feature_requests():
    """List all feature requests with filtering"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status', None)  # Filter by status
    
    query = FeatureRequest.query
    
    if status:
        query = query.filter_by(status=status)
    
    results = query.order_by(
        FeatureRequest.votes.desc(),
        FeatureRequest.created_at.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'data': [f.to_dict() for f in results.items],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': results.total,
            'pages': results.pages
        }
    }), 200

@feedback_bp.route('/stats', methods=['GET'])
def get_feedback_stats():
    """Get comprehensive feedback statistics"""
    total_feedback = Feedback.query.count()
    avg_rating = db.session.query(db.func.avg(Feedback.rating)).scalar() or 0
    
    feedback_by_type = db.session.query(
        Feedback.feedback_type,
        db.func.count(Feedback.id)
    ).group_by(Feedback.feedback_type).all()
    
    ratings_distribution = db.session.query(
        Feedback.rating,
        db.func.count(Feedback.id)
    ).group_by(Feedback.rating).all()
    
    return jsonify({
        'total_feedback': total_feedback,
        'average_rating': round(avg_rating, 1),
        'feedback_by_type': {type_name: count for type_name, count in feedback_by_type},
        'ratings_distribution': {rating: count for rating, count in ratings_distribution},
        'timestamp': datetime.utcnow().isoformat()
    }), 200