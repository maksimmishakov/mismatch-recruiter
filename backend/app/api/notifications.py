"""Notification endpoints."""
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
    user_id = get_jwt_identity()
    limit = request.args.get('limit', 20, type=int)
    offset = request.args.get('offset', 0, type=int)
   
    try:
        notifications = Notification.query.filter_by(
            user_id=user_id
        ).order_by(
            Notification.created_at.desc()
        ).limit(limit).offset(offset).all()
       
        total = Notification.query.filter_by(user_id=user_id).count()
        unread = Notification.query.filter_by(
            user_id=user_id,
            read=False
        ).count()
       
        return jsonify({
            'notifications': [n.to_dict() for n in notifications],
            'total': total,
            'unread': unread,
        }), 200
   
    except Exception as e:
        logger.error(f"Error fetching notifications: {e}")
        return jsonify({'error': str(e)}), 500

@bp.route('/mark-read/<int:notification_id>', methods=['POST'])
@jwt_required()
def mark_read(notification_id):
    """Mark notification as read."""
    user_id = get_jwt_identity()
   
    try:
        notification = Notification.query.filter_by(
            id=notification_id,
            user_id=user_id
        ).first_or_404()
       
        notification.read = True
        db.session.commit()
       
        return jsonify(notification.to_dict()), 200
   
    except Exception as e:
        logger.error(f"Error marking notification as read: {e}")
        return jsonify({'error': str(e)}), 500

@bp.route('/mark-all-read', methods=['POST'])
@jwt_required()
def mark_all_read():
    """Mark all notifications as read."""
    user_id = get_jwt_identity()
   
    try:
        Notification.query.filter_by(
            user_id=user_id,
            read=False
        ).update({'read': True})
        db.session.commit()
       
        return jsonify({'success': True}), 200
   
    except Exception as e:
        logger.error(f"Error marking all as read: {e}")
        return jsonify({'error': str(e)}), 500