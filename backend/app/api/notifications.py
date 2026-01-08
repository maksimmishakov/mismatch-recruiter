"""Notification API endpoints."""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Notification, db
import logging

bp = Blueprint('notifications', __name__, url_prefix='/api/notifications')
logger = logging.getLogger(__name__)

@bp.route('/list', methods=['GET'])
@jwt_required()
def list_notifications():
    """Get user notifications."""
    userid = get_jwt_identity()
    limit = int(request.args.get('limit', 20))
    offset = int(request.args.get('offset', 0))
    
    try:
        notifications = Notification.query.filter_by(userid=userid) \
            .order_by(Notification.created_at.desc()) \
            .limit(limit).offset(offset).all()
        total = Notification.query.filter_by(userid=userid).count()
        unread = Notification.query.filter_by(userid=userid, read=False).count()
        
        return jsonify({
            'notifications': [n.to_dict() for n in notifications],
            'total': total,
            'unread': unread
        }), 200
    except Exception as e:
        logger.error(f'Error fetching notifications: {e}')
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:notification_id>/mark-read', methods=['POST'])
@jwt_required()
def mark_read(notification_id):
    """Mark notification as read."""
    userid = get_jwt_identity()
    try:
        notification = Notification.query.filter_by(id=notification_id, userid=userid).first_or_404()
        notification.read = True
        db.session.commit()
        return jsonify(notification.to_dict()), 200
    except Exception as e:
        logger.error(f'Error marking notification as read: {e}')
        return jsonify({'error': str(e)}), 500

@bp.route('/mark-all-read', methods=['POST'])
@jwt_required()
def mark_all_read():
    """Mark all notifications as read."""
    userid = get_jwt_identity()
    try:
        Notification.query.filter_by(userid=userid, read=False).update({'read': True})
        db.session.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        logger.error(f'Error marking all as read: {e}')
        return jsonify({'error': str(e)}), 500
