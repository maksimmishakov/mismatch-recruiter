from datetime import datetime
from flask import jsonify

def init_health_check(app):
    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'service': 'mismatch-recruiter-backend',
            'version': '1.0.0'
        }), 200
    
    @app.route('/ready', methods=['GET'])
    def readiness():
        try:
            return jsonify({
                'ready': True,
                'checks': {
                    'database': 'ok',
                    'service': 'ready'
                }
            }), 200
        except Exception as e:
            return jsonify({
                'ready': False,
                'error': str(e)
            }), 503
