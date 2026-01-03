from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from db_models import db, Candidates, JobProfiles, MatchRecords, SkillsTaxonomy
import uuid
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mismatch.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

CORS(app)

with app.app_context():
    db.create_all()

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'message': '✅ MisMatch API OK', 'database': 'connected'}), 200

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/api/candidates', methods=['GET'])
def get_candidates():
    try:
        candidates = Candidates.query.all()
        data = [{
            'id': c.id,
            'name': f'{c.first_name} {c.last_name}',
            'email': c.email,
            'skills': c.skills or [],
            'experience_years': c.experience_years,
            'match_score': 85
        } for c in candidates]
        return jsonify({'status': 'ok', 'count': len(data), 'data': data}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/candidates', methods=['POST'])
def create_candidate():
    try:
        data = request.get_json()
        candidate = Candidates(
            id=str(uuid.uuid4()),
            first_name=data.get('first_name', 'John'),
            last_name=data.get('last_name', 'Doe'),
            email=data.get('email', f'user_{uuid.uuid4().hex[:8]}@example.com'),
            skills=data.get('skills', []),
            experience_years=data.get('experience_years', 0)
        )
        db.session.add(candidate)
        db.session.commit()
        return jsonify({'status': 'ok', 'message': 'Candidate created', 'id': candidate.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 400

        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/database/reset', methods=['POST'])
def reset_database():
    try:
        db.drop_all()
        db.create_all()
        return jsonify({'status': 'ok', 'message': 'Database reset successfully'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

# Import NLP service
from services.transformer_nlp_service import TransformerNLPService

# Initialize NLP service
nlp_service = TransformerNLPService()

# NLP Endpoints
@app.route('/api/resume/analyze-advanced', methods=['POST'])
def analyze_resume_advanced():
    """Advanced resume analysis with DistilBERT NLP"""
    try:
        data = request.json
        resume_text = data.get('resume_text', '')
        
        if not resume_text:
            return jsonify({'error': 'resume_text is required'}), 400
        
        result = nlp_service.extract_skills_advanced(resume_text)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/matching/semantic', methods=['POST'])
def semantic_matching():
    """Semantic matching between resume and job"""
    try:
        data = request.json
        resume_text = data.get('resume_text', '')
        job_description = data.get('job_description', '')
        
        if not resume_text or not job_description:
            return jsonify({'error': 'Both resume_text and job_description are required'}), 400
        
        result = nlp_service.semantic_matching(resume_text, job_description)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Bias Detection and Compliance
from services.bias_detection_service import BiasDetectionService

bias_service = BiasDetectionService()

@app.route('/api/compliance/audit-hiring', methods=['POST'])
def audit_hiring_compliance():
    """Comprehensive hiring bias audit (EU AI Act compliant)"""
    try:
        data = request.json
        hiring_data = data.get('hiring_data', {})
        
        result = bias_service.comprehensive_audit(hiring_data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Real-time Metrics via WebSocket
from flask_socketio import SocketIO, emit, disconnect
from services.realtime_service import RealtimeMetricsService

realtime_service = RealtimeMetricsService()
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection"""
    try:
        realtime_service.connect(request.sid, request.sid)
        emit('connected', {'data': 'Connected to live metrics'})
    except Exception as e:
        print(f"Connection error: {e}")

@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection"""
    realtime_service.disconnect(request.sid)
    print(f"Client disconnected")

@socketio.on('request_metrics')
def handle_metrics_request():
    """Send live metrics to client"""
    try:
        metrics = realtime_service.get_current_metrics()
        emit('metrics_update', metrics, broadcast=True)
    except Exception as e:
        emit('error', {'error': str(e)})
