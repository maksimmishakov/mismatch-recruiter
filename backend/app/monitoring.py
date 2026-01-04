from flask import Blueprint, jsonify
from prometheus_client import Counter, Histogram, Gauge, generate_latest, REGISTRY
import time
import os

monitoring_bp = Blueprint('monitoring', __name__, url_prefix='/metrics')

# Prometheus metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

db_queries_total = Counter(
    'db_queries_total',
    'Total database queries',
    ['operation', 'table']
)

db_query_duration_seconds = Histogram(
    'db_query_duration_seconds',
    'Database query duration in seconds',
    ['operation', 'table']
)

matches_created_total = Counter(
    'matches_created_total',
    'Total matches created',
    ['source']
)

active_connections = Gauge(
    'active_connections',
    'Number of active database connections'
)

@monitoring_bp.route('/health', methods=['GET'])
def health_check():
    """
    Kubernetes-friendly liveness and readiness probe endpoint.
    """
    return jsonify({
        'status': 'ok',
        'service': 'mismatch-recruiter-api',
        'version': os.getenv('VERSION', '0.0.1')
    }), 200

@monitoring_bp.route('/ready', methods=['GET'])
def readiness_probe():
    """
    Readiness probe to check if service is ready for traffic.
    """
    try:
        from app.models import db
        # Check database connection
        db.session.execute('SELECT 1')
        return jsonify({
            'ready': True,
            'checks': {
                'database': 'ok',
                'memory': 'ok'
            }
        }), 200
    except Exception as e:
        return jsonify({
            'ready': False,
            'error': str(e)
        }), 503

@monitoring_bp.route('/prometheus', methods=['GET'])
def prometheus_metrics():
    """
    Prometheus metrics endpoint (text format).
    """
    return generate_latest(REGISTRY).decode('utf-8'), 200, {'Content-Type': 'text/plain'}

@monitoring_bp.route('/live', methods=['GET'])
def liveness_probe():
    """
    Liveness probe - indicates if the service should be restarted.
    """
    return jsonify({'alive': True}), 200

def init_monitoring(app):
    """
    Initialize monitoring for Flask application.
    """
    app.register_blueprint(monitoring_bp)
    
    @app.before_request
    def before_request():
        from flask import request, g
        g.start_time = time.time()
        g.request_start = g.start_time
    
    @app.after_request
    def after_request(response):
        from flask import request, g
        
        if hasattr(g, 'start_time'):
            duration = time.time() - g.start_time
            http_request_duration_seconds.labels(
                method=request.method,
                endpoint=request.endpoint or 'unknown'
            ).observe(duration)
            
            http_requests_total.labels(
                method=request.method,
                endpoint=request.endpoint or 'unknown',
                status=response.status_code
            ).inc()
        
        return response
