"""Webhooks API routes with registration, delivery, and event history."""

from flask import Blueprint, request, jsonify
from app.database import SessionLocal
from app.models import Webhook, WebhookEvent
from app.services.webhook_service import WebhookService
from app.logger import get_logger
from datetime import datetime
import json

logger = get_logger("webhooks")
webhooks_bp = Blueprint('webhooks', __name__, url_prefix='/api/webhooks')
webhook_service = WebhookService()


@webhooks_bp.route('/register', methods=['POST'])
def register_webhook():
    """Register a new webhook subscription."""
    try:
        data = request.get_json()
        if not all(k in data for k in ['user_id', 'url', 'events']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        db = SessionLocal()
        webhook = Webhook(
            user_id=data['user_id'],
            url=data['url'],
            events=','.join(data['events']),
            secret=data.get('secret', ''),
            is_active=True
        )
        db.add(webhook)
        db.commit()
        webhook_id = webhook.id
        db.close()
        
        logger.info(f"Webhook registered: {webhook_id}")
        return jsonify({
            'id': webhook_id,
            'url': webhook.url,
            'events': webhook.events.split(','),
            'is_active': webhook.is_active
        }), 201
    except Exception as e:
        logger.error(f"Error registering webhook: {e}")
        return jsonify({'error': str(e)}), 500


@webhooks_bp.route('/<int:webhook_id>', methods=['GET'])
def get_webhook(webhook_id):
    """Get webhook details by ID."""
    try:
        db = SessionLocal()
        webhook = db.query(Webhook).filter(Webhook.id == webhook_id).first()
        db.close()
        
        if not webhook:
            return jsonify({'error': 'Webhook not found'}), 404
        
        return jsonify({
            'id': webhook.id,
            'url': webhook.url,
            'events': webhook.events.split(','),
            'is_active': webhook.is_active,
            'created_at': webhook.created_at.isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({'error': str(e)}), 500


@webhooks_bp.route('/<int:webhook_id>', methods=['DELETE'])
def delete_webhook(webhook_id):
    """Delete a webhook subscription."""
    try:
        db = SessionLocal()
        webhook = db.query(Webhook).filter(Webhook.id == webhook_id).first()
        if not webhook:
            db.close()
            return jsonify({'error': 'Webhook not found'}), 404
        
        db.delete(webhook)
        db.commit()
        db.close()
        
        logger.info(f"Webhook deleted: {webhook_id}")
        return jsonify({'message': 'Webhook deleted'}), 200
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({'error': str(e)}), 500


@webhooks_bp.route('', methods=['GET'])
def list_webhooks():
    """List all webhooks for a user."""
    try:
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            return jsonify({'error': 'user_id required'}), 400
        
        db = SessionLocal()
        webhooks = db.query(Webhook).filter(Webhook.user_id == user_id).all()
        db.close()
        
        return jsonify({
            'webhooks': [{
                'id': w.id,
                'url': w.url,
                'events': w.events.split(','),
                'is_active': w.is_active
            } for w in webhooks],
            'count': len(webhooks)
        }), 200
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({'error': str(e)}), 500


@webhooks_bp.route('/test/<int:webhook_id>', methods=['POST'])
def test_webhook(webhook_id):
    """Send test webhook payload."""
    try:
        db = SessionLocal()
        webhook = db.query(Webhook).filter(Webhook.id == webhook_id).first()
        if not webhook:
            db.close()
            return jsonify({'error': 'Webhook not found'}), 404
        
        test_payload = {
            'event': 'webhook.test',
            'timestamp': datetime.utcnow().isoformat(),
            'data': {'message': 'Test webhook'}
        }
        
        result = webhook_service.send_webhook(webhook, test_payload)
        
        event = WebhookEvent(
            webhook_id=webhook_id,
            event_type='webhook.test',
            payload=json.dumps(test_payload),
            status='sent' if result['success'] else 'failed',
            response_status=result.get('status_code', 0)
        )
        db.add(event)
        db.commit()
        db.close()
        
        logger.info(f"Test webhook sent: {webhook_id}")
        return jsonify(result), 200 if result['success'] else 500
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({'error': str(e)}), 500
