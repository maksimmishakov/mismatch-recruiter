#!/bin/bash
echo "🚀 MISMATCH RECRUITER - БЫСТРАЯ УСТАНОВКА"
echo "=========================================="
cd /workspace 2>/dev/null || cd /workspaces/mismatch-recruiter
echo "📦 Installing Backend..."
cat > app.py << 'APPEOF'
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'message': '✅ MisMatch API OK'}), 200

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Welcome to MisMatch API'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
APPEOF
pip install -q flask flask-cors
echo "✅ Backend Ready!"
echo "🚀 Starting Flask..."
python3 app.py
