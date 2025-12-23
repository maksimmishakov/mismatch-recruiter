import os
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from datetime import datetime
from werkzeug.utils import secure_filename
from twilio.rest import Client

from llm_client import LLMClient

# Инициализируй клиент при старте
try:
    llm_client = LLMClient()
except RuntimeError as e:
    print(f"Warning: LLM client initialization failed: {e}")
    llm_client = None

load_dotenv()

app = Flask(__name__)

# ==================== ÊÎÍÔÈÃÓÐÀÖÈß ====================

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///MisMatch.db')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-change-in-prod')

# Êîíôèãóðàöèÿ çàãðóçîê
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Twilio äëÿ WhatsApp
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', 'test')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', 'test')
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER', '+14155552671')

db = SQLAlchemy(app)

# ==================== ÌÎÄÅËÈ ====================

class Candidate(db.Model):
    '''Ìîäåëü êàíäèäàòà'''
    __tablename__ = 'candidates'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    position = db.Column(db.String(255))
    skills = db.Column(db.JSON, default=list)
    score = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(50), default='pending')
    red_flags = db.Column(db.JSON, default=list)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'position': self.position,
            'skills': self.skills,
            'score': self.score,
            'status': self.status,
            'red_flags': self.red_flags,
            'date_added': self.date_added.isoformat() if self.date_added else None
        }

# ==================== ÂÑÏÎÌÎÃÀÒÅËÜÍÛÅ ÔÓÍÊÖÈÈ ====================

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def detect_red_flags(candidate):
    '''Âûÿâëÿåò ïîäîçðèòåëüíûå ñèãíàëû â ðåçþìå'''
    red_flags = []
    
    if not candidate.email or '@' not in str(candidate.email):
        red_flags.append('invalid_email')
    
    if not candidate.position or candidate.position == 'Íà ðàññìîòðåíèè':
        red_flags.append('no_position_specified')
    
    if candidate.score > 90:
        red_flags.append('suspiciously_high_score')
    
    if not candidate.phone:
        red_flags.append('no_phone_provided')
    
    return {
        'has_flags': len(red_flags) > 0,
        'flags': red_flags,
        'risk_level': 'HIGH' if len(red_flags) > 2 else 'MEDIUM' if len(red_flags) > 0 else 'LOW'
    }

def find_duplicate_candidates(candidate_id):
    '''Íàõîäèò äóáëèêàòû ðåçþìå'''
    candidate = Candidate.query.get(candidate_id)
    if not candidate:
        return []
    
    similar_candidates = Candidate.query.filter(
        Candidate.name.ilike(f'%{candidate.name.split()[0] if candidate.name else ""}%'),
        Candidate.id != candidate_id
    ).all()
    
    duplicates = []
    for similar in similar_candidates:
        if (similar.email and candidate.email and similar.email == candidate.email) or \
           (similar.skills == candidate.skills and len(similar.skills) > 0):
            duplicates.append(similar.to_dict())
    
    return duplicates

def send_whatsapp_notification(phone, candidate_name, status):
    '''Îòïðàâëÿåò WhatsApp óâåäîìëåíèå'''
    try:
        if not TWILIO_ACCOUNT_SID or TWILIO_ACCOUNT_SID == 'test':
            return {'status': 'demo_mode', 'message': 'WhatsApp (demo mode)'}
        
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        if status == 'approved':
            text = f'Ïðèâåò {candidate_name}! ?? Òâî¸ ðåçþìå ïðîøëî ïåðâûé òóð! Ïîäðîáíîñòè ïî ïî÷òå.'
        elif status == 'rejected':
            text = f'Ñïàñèáî {candidate_name}! Ìû ðàññìîòðåëè òâî¸ ðåçþìå. Óäà÷è! ??'
        else:
            text = f'Ïðèâåò {candidate_name}! Òâî¸ ðåçþìå â îáðàáîòêå.'
        
        message = client.messages.create(
            from_=f'whatsapp:{TWILIO_WHATSAPP_NUMBER}',
            body=text,
            to=f'whatsapp:{phone}'
        )
        return {'status': 'sent', 'message_id': message.sid}
    except Exception as e:
        return {'status': 'error', 'error': str(e)}

# ==================== ROUTES ====================

@app.route('/')
def index():
    return jsonify({
        'message': 'MisMatch API is running!',
        'version': '1.0.1',
        'features': ['upload', 'red_flags', 'duplicates', 'whatsapp_notify'],
        'endpoints': {
            'ui': '/upload',
            'health': '/api/health',
            'candidates': '/api/candidates',
            'candidate': '/api/candidate/<id>',
            'red_flags': '/api/candidate/<id>/red-flags',
            'duplicates': '/api/candidates/find-duplicates/<id>',
            'notify': '/api/candidate/<id>/notify',
            'upload': 'POST /api/upload'
        }
    })

@app.route('/api/status')
def status():
    return {'status': 'ok', 'timestamp': datetime.now().isoformat()}

@app.route('/api/health', methods=['GET'])
def health():
    try:
        db.session.execute('SELECT 1')
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'database': 'disconnected'
        }), 500

@app.route('/api/candidates', methods=['GET'])
def get_candidates():
    try:
        candidates = Candidate.query.order_by(Candidate.score.desc()).all()
        return jsonify({
            'candidates': [c.to_dict() for c in candidates],
            'count': len(candidates)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/candidate/<int:candidate_id>', methods=['GET'])
def get_candidate(candidate_id):
    try:
        candidate = Candidate.query.get(candidate_id)
        if not candidate:
            return jsonify({'error': 'Candidate not found'}), 404
        return jsonify(candidate.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/candidate/<int:candidate_id>/red-flags', methods=['GET'])
def get_candidate_flags(candidate_id):
    '''Ïîëó÷èòü êðàñíûå ôëàãè êàíäèäàòà'''
    try:
        candidate = Candidate.query.get(candidate_id)
        if not candidate:
            return jsonify({'error': 'Candidate not found'}), 404
        
        flags = detect_red_flags(candidate)
        return jsonify({
            'candidate_id': candidate.id,
            'candidate_name': candidate.name,
            'red_flags': flags
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/candidates/find-duplicates/<int:candidate_id>', methods=['GET'])
def find_duplicates(candidate_id):
    '''Íàéòè äóáëèêàòû ðåçþìå'''
    try:
        duplicates = find_duplicate_candidates(candidate_id)
        candidate = Candidate.query.get(candidate_id)
        
        return jsonify({
            'candidate_id': candidate_id,
            'candidate_name': candidate.name if candidate else 'Unknown',
            'duplicates_found': len(duplicates),
            'duplicates': duplicates
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/candidate/<int:candidate_id>/notify', methods=['POST'])
def notify_candidate(candidate_id):
    '''Îòïðàâèòü WhatsApp óâåäîìëåíèå'''
    try:
        data = request.get_json()
        candidate = Candidate.query.get(candidate_id)
        
        if not candidate:
            return jsonify({'error': 'Candidate not found'}), 404
        
        phone = data.get('phone') or candidate.phone
        status = data.get('status', 'pending')
        
        if not phone:
            return jsonify({'error': 'Phone number required'}), 400
        
        result = send_whatsapp_notification(phone, candidate.name, status)
        
        return jsonify({
            'success': result.get('status') in ['sent', 'demo_mode'],
            'result': result,
            'candidate': candidate.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/candidate', methods=['POST'])
def create_candidate():
    try:
        data = request.get_json()

        candidate = Candidate(
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            position=data.get('position'),
            skills=data.get('skills', []),
            score=data.get('score', 0.0),
            status='pending'
        )

        candidate.red_flags = detect_red_flags(candidate).get('flags', [])

        db.session.add(candidate)
        db.session.commit()

        return jsonify({
            'success': True,
            'candidate_id': candidate.id,
            'candidate': candidate.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/upload')
def upload_page():
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_resume():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'Empty filename'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400

        filename = secure_filename(file.filename)
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        candidate_name = file.filename.rsplit('.', 1)[0]
        candidate = Candidate(
            name=candidate_name,
            position='Íà ðàññìîòðåíèè',
            skills=['python', 'javascript'],
            score=75.0,
            status='pending'
        )

        candidate.red_flags = detect_red_flags(candidate).get('flags', [])

        db.session.add(candidate)
        db.session.commit()

        return jsonify({
            'success': True,
            'candidate_id': candidate.id,
            'message': f'Êàíäèäàò {candidate_name} äîáàâëåí',
            'candidate': candidate.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze-resume-ai/<int:candidate_id>', methods=['POST'])
def analyze_resume_with_ai(candidate_id):
    """Анализирует резюме с помощью AI через ProxyAPI."""
    try:
        if llm_client is None:
            return jsonify({'error': 'LLM service not available'}), 503
        
        candidate = Candidate.query.get(candidate_id)
        if not candidate:
            return jsonify({'error': 'Candidate not found'}), 404
        
        # Получить текст резюме
        resume_text = f"Имя: {candidate.name}\nДолжность: {candidate.position}\nНавыки: {', '.join(candidate.skills) if candidate.skills else 'N/A'}"
        
        # Анализировать через LLM
        ai_data = llm_client.analyze_resume(resume_text)
        
        # Обновить score и skills
        candidate.score = ai_data.get('score', candidate.score)
        candidate.skills = ai_data.get('skills', candidate.skills)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'candidate_id': candidate_id,
            'ai_analysis': ai_data,
            'candidate': candidate.to_dict()
        }), 200
        
    except RuntimeError as e:
        return jsonify({'error': f'AI analysis error: {str(e)}'}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)


# ==================== BATCH UPLOAD & JOB MATCHING ====================

@app.route('/batch', methods=['GET'])
def batch_upload_page():
    """Render batch upload page"""
    return render_template('batch_upload.html')


@app.route('/api/batch/upload', methods=['POST'])
def batch_upload_files():
    """Handle batch file upload and parsing"""
    try:
        if 'files' not in request.files:
            return jsonify({'error': 'No files provided'}), 400
        
        files = request.files.getlist('files')
        results = []
        
        for file in files:
            if file and file.filename:
                filename = secure_filename(file.filename)
                ext = os.path.splitext(filename)[1].lower()
                
                if ext not in ['.pdf', '.docx', '.doc']:
                    results.append({
                        'filename': filename,
                        'success': False,
                        'error': 'Unsupported file format'
                    })
                    continue
                
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                try:
                    from utils.file_parser import parse_file
                    content = parse_file(filepath)
                    results.append({
                        'filename': filename,
                        'success': True,
                        'content_preview': content[:200] if content else 'No content extracted'
                    })
                except Exception as e:
                    results.append({
                        'filename': filename,
                        'success': False,
                        'error': str(e)
                    })
        
        return jsonify({
            'success': True,
            'total_files': len(files),
            'successful': len([r for r in results if r['success']]),
            'results': results
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/batch/process', methods=['POST'])
def batch_process_files():
    """Process batch files with AI analysis and embeddings"""
    try:
        data = request.get_json()
        files_data = data.get('files', [])
        results = []
        
        for file_data in files_data:
            filename = file_data.get('filename')
            content = file_data.get('content')
            
            if not content:
                continue
            
            try:
                ai_analysis = llm_client.analyze_resume(content)
                
                try:
                    from sentence_transformers import SentenceTransformer
                    model = SentenceTransformer('all-MiniLM-L6-v2')
                    embeddings = model.encode(content).tolist()
                except:
                    embeddings = []
                
                results.append({
                    'filename': filename,
                    'analysis': ai_analysis,
                    'embeddings': embeddings
                })
            except Exception as e:
                results.append({
                    'filename': filename,
                    'error': str(e)
                })
        
        return jsonify({
            'success': True,
            'total_files': len(files_data),
            'processed': len(results),
            'results': results
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/job-matcher', methods=['POST'])
def job_matcher_endpoint():
    """Match jobs with candidates based on skills and experience"""
    try:
        data = request.get_json()
        job_description = data.get('job_description')
        candidates = data.get('candidates', [])
        
        if not job_description:
            return jsonify({'error': 'Job description is required'}), 400
        
        try:
            job_analysis = llm_client.analyze_job(job_description)
        except:
            job_analysis = {'skills': [], 'requirements': []}
        
        matches = []
        
        for candidate in candidates:
            candidate_id = candidate.get('id')
            candidate_data = candidate.get('data', {})
            
            try:
                score = llm_client.match_candidate(job_analysis, candidate_data)
            except:
                score = 0.0
            
            if score >= 0.7:
                matches.append({
                    'candidate_id': candidate_id,
                    'match_score': round(score, 2),
                    'match_percentage': f"{score * 100:.1f}%"
                })
        
        matches.sort(key=lambda x: x['match_score'], reverse=True)
        
        return jsonify({
            'success': True,
            'job_analysis': job_analysis,
            'total_candidates': len(candidates),
            'matched_count': len(matches),
            'matches': matches[:10]
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
