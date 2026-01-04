import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv('.env.dev')

app = Flask(__name__)

# CORS конфигурация
CORS(app, origins=['http://localhost:5173', 'http://localhost:3000'])

@app.route('/health', methods=['GET'])
def health():
    """Endpoint для проверки здоровья сервера"""
    return jsonify({'status': 'ok', 'service': 'MisMatch Recruiter API'}), 200

@app.route('/api', methods=['GET'])
def api_info():
    """API информация"""
    return jsonify({
        'name': 'MisMatch Recruiter API',
        'version': '1.0.0',
        'status': 'running'
    }), 200

if __name__ == '__main__':
    port = int(os.getenv('SERVER_PORT', 8000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
