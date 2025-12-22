import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from datetime import datetime

# Загружаем переменные окружения
load_dotenv()

app = Flask(__name__)

# ==================== КОНФИГУРАЦИЯ ====================

# Получаем DATABASE_URL из переменных окружения Amvera
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///rankpo.db')

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-change-in-prod')

# Инициализируем БД
db = SQLAlchemy(app)

# ==================== МОДЕЛИ ====================

class Candidate(db.Model):
    '''Модель кандидата'''
    __tablename__ = 'candidates'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255))
    position = db.Column(db.String(255))
    skills = db.Column(db.JSON, default=list)
    score = db.Column(db.Float, default=0.0)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'position': self.position,
            'skills': self.skills,
            'score': self.score,
            'date_added': self.date_added.isoformat() if self.date_added else None
        }

# ==================== ROUTES ====================

@app.route('/')
def index():
    '''Главная страница'''
    return jsonify({
        'message': 'RankPO API is running!',
        'version': '1.0.0',
        'endpoints': {
            'health': '/api/health',
            'candidates': '/api/candidates',
            'candidate': '/api/candidate/<id>',
            'create_candidate': 'POST /api/candidate'
        }
    })

@app.route('/api/status')
def status():
    '''Status endpoint (старый, для совместимости)'''
    return {'status': 'ok', 'timestamp': datetime.now().isoformat()}

@app.route('/api/health', methods=['GET'])
def health():
    '''Health check для Amvera'''
    try:
        # Проверяем БД
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
    '''Получить всех кандидатов'''
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
    '''Получить кандидата по ID'''
    try:
        candidate = Candidate.query.get(candidate_id)
        if not candidate:
            return jsonify({'error': 'Candidate not found'}), 404
        return jsonify(candidate.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/candidate', methods=['POST'])
def create_candidate():
    '''Создать кандидата'''
    try:
        data = request.get_json()
        
        candidate = Candidate(
            name=data.get('name'),
            email=data.get('email'),
            position=data.get('position'),
            skills=data.get('skills', []),
            score=data.get('score', 0.0)
        )
        
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

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# ==================== INITIALIZATION ====================

with app.app_context():
    db.create_all()

# ==================== MAIN ====================

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
