# 🎯 КРИТИЧЕСКИЙ ПЛАН ДЕЙСТВИЙ - 10 ЯНВАРЯ 2026

**Статус:** URGENT - ALL WORKFLOWS FAILING (52+ GitHub Actions errors)  
**Root Cause:** Missing blueprint modules (auth.py, candidates.py, jobs.py)  
**Deadline:** 14 января, 14:00 MSK для демо Lamoda  
**Estimated Time to Fix:** 4 часа

---

## 🔴 ТЕКУЩАЯ СИТУАЦИЯ

### Что упало?
```
❌ Backend Tests - FAILED
❌ Backend Tests & Build - FAILED
❌ CI/CD Pipeline - FAILED
❌ Frontend Tests - FAILED

Все 52 ошибки происходят из одной причины:
ModuleNotFoundError: No module named 'app.routes.auth'
```

### Почему упало?
```
conftest.py пытается импортировать:
  from app.routes.auth import auth_bp
  from app.routes.candidates import candidates_bp
  from app.routes.jobs import jobs_bp

НО ЭТИ ФАЙЛЫ НЕ СУЩЕСТВУЮТ!
Папка app/routes/ пуста (кроме __init__.py)
```

---

## ✅ РЕШЕНИЕ - 4 ШАГА (4 ЧАСА)

### ШАГ 1: Создать auth.py (20 минут)
**Путь:** `backend/app/routes/auth.py`

```python
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """Регистрация нового пользователя"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password required'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'User with this email already exists'}), 409
    
    user = User(
        email=data['email'],
        first_name=data.get('first_name', 'User'),
        last_name=data.get('last_name', ''),
        role=data.get('role', 'RECRUITER')
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'message': 'User registered successfully',
        'access_token': access_token,
        'user': {
            'id': user.id,
            'email': user.email,
            'role': user.role
        }
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """Вход в систему"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password required'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'user': {
            'id': user.id,
            'email': user.email,
            'role': user.role
        }
    }), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Получить текущего пользователя"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'id': user.id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'role': user.role
    }), 200
```

### ШАГ 2: Создать candidates.py (20 минут)
**Путь:** `backend/app/routes/candidates.py`

```python
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.candidate import Candidate

candidates_bp = Blueprint('candidates', __name__, url_prefix='/api/candidates')

@candidates_bp.route('', methods=['GET'])
@jwt_required()
def list_candidates():
    """Получить список кандидатов"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    candidates = Candidate.query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'candidates': [{
            'id': c.id,
            'first_name': c.first_name,
            'last_name': c.last_name,
            'email': c.email,
            'skills': c.skills or [],
            'experience_years': c.experience_years
        } for c in candidates.items],
        'total': candidates.total,
        'pages': candidates.pages,
        'current_page': page
    }), 200

@candidates_bp.route('/<int:candidate_id>', methods=['GET'])
@jwt_required()
def get_candidate(candidate_id):
    """Получить кандидата"""
    candidate = Candidate.query.get_or_404(candidate_id)
    
    return jsonify({
        'id': candidate.id,
        'first_name': candidate.first_name,
        'last_name': candidate.last_name,
        'email': candidate.email,
        'skills': candidate.skills or [],
        'experience_years': candidate.experience_years
    }), 200

@candidates_bp.route('', methods=['POST'])
@jwt_required()
def create_candidate():
    """Создать кандидата"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or not data.get('email'):
        return jsonify({'error': 'Email is required'}), 400
    
    candidate = Candidate(
        recruiter_id=current_user_id,
        first_name=data.get('first_name', ''),
        last_name=data.get('last_name', ''),
        email=data['email'],
        skills=data.get('skills', []),
        experience_years=data.get('experience_years', 0)
    )
    
    db.session.add(candidate)
    db.session.commit()
    
    return jsonify({
        'message': 'Candidate created',
        'id': candidate.id
    }), 201

@candidates_bp.route('/<int:candidate_id>', methods=['PUT'])
@jwt_required()
def update_candidate(candidate_id):
    """Обновить кандидата"""
    current_user_id = get_jwt_identity()
    candidate = Candidate.query.get_or_404(candidate_id)
    
    if candidate.recruiter_id != current_user_id:
        return jsonify({'error': 'Forbidden'}), 403
    
    data = request.get_json()
    candidate.first_name = data.get('first_name', candidate.first_name)
    candidate.last_name = data.get('last_name', candidate.last_name)
    candidate.skills = data.get('skills', candidate.skills)
    candidate.experience_years = data.get('experience_years', candidate.experience_years)
    
    db.session.commit()
    
    return jsonify({'message': 'Candidate updated'}), 200

@candidates_bp.route('/<int:candidate_id>', methods=['DELETE'])
@jwt_required()
def delete_candidate(candidate_id):
    """Удалить кандидата"""
    current_user_id = get_jwt_identity()
    candidate = Candidate.query.get_or_404(candidate_id)
    
    if candidate.recruiter_id != current_user_id:
        return jsonify({'error': 'Forbidden'}), 403
    
    db.session.delete(candidate)
    db.session.commit()
    
    return jsonify({'message': 'Candidate deleted'}), 200
```

### ШАГ 3: Создать jobs.py (20 минут)
**Путь:** `backend/app/routes/jobs.py`

```python
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.job import Job

jobs_bp = Blueprint('jobs', __name__, url_prefix='/api/jobs')

@jobs_bp.route('', methods=['GET'])
@jwt_required()
def list_jobs():
    """Получить список вакансий"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    jobs = Job.query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'jobs': [{
            'id': j.id,
            'title': j.title,
            'description': j.description,
            'location': j.location,
            'salary_min': j.salary_min,
            'salary_max': j.salary_max,
            'required_skills': j.required_skills or [],
            'experience_years_min': j.experience_years_min,
            'status': j.status
        } for j in jobs.items],
        'total': jobs.total,
        'pages': jobs.pages,
        'current_page': page
    }), 200

@jobs_bp.route('/<int:job_id>', methods=['GET'])
@jwt_required()
def get_job(job_id):
    """Получить вакансию"""
    job = Job.query.get_or_404(job_id)
    
    return jsonify({
        'id': job.id,
        'title': job.title,
        'description': job.description,
        'location': job.location,
        'salary_min': job.salary_min,
        'salary_max': job.salary_max,
        'required_skills': job.required_skills or [],
        'experience_years_min': job.experience_years_min,
        'status': job.status
    }), 200

@jobs_bp.route('', methods=['POST'])
@jwt_required()
def create_job():
    """Создать вакансию"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400
    
    job = Job(
        recruiter_id=current_user_id,
        title=data['title'],
        description=data.get('description', ''),
        location=data.get('location', ''),
        salary_min=data.get('salary_min'),
        salary_max=data.get('salary_max'),
        required_skills=data.get('required_skills', []),
        experience_years_min=data.get('experience_years_min', 0),
        status='OPEN'
    )
    
    db.session.add(job)
    db.session.commit()
    
    return jsonify({
        'message': 'Job created',
        'id': job.id
    }), 201

@jobs_bp.route('/<int:job_id>', methods=['PUT'])
@jwt_required()
def update_job(job_id):
    """Обновить вакансию"""
    current_user_id = get_jwt_identity()
    job = Job.query.get_or_404(job_id)
    
    if job.recruiter_id != current_user_id:
        return jsonify({'error': 'Forbidden'}), 403
    
    data = request.get_json()
    job.title = data.get('title', job.title)
    job.description = data.get('description', job.description)
    job.location = data.get('location', job.location)
    job.salary_min = data.get('salary_min', job.salary_min)
    job.salary_max = data.get('salary_max', job.salary_max)
    job.required_skills = data.get('required_skills', job.required_skills)
    job.experience_years_min = data.get('experience_years_min', job.experience_years_min)
    job.status = data.get('status', job.status)
    
    db.session.commit()
    
    return jsonify({'message': 'Job updated'}), 200

@jobs_bp.route('/<int:job_id>', methods=['DELETE'])
@jwt_required()
def delete_job(job_id):
    """Удалить вакансию"""
    current_user_id = get_jwt_identity()
    job = Job.query.get_or_404(job_id)
    
    if job.recruiter_id != current_user_id:
        return jsonify({'error': 'Forbidden'}), 403
    
    job.status = 'CLOSED'
    db.session.commit()
    
    return jsonify({'message': 'Job deleted'}), 200
```

### ШАГ 4: Обновить app/routes/__init__.py (10 минут)

```python
from flask import Blueprint

# Import blueprints
from app.routes.auth import auth_bp
from app.routes.candidates import candidates_bp
from app.routes.jobs import jobs_bp

# Export for registration
__all__ = ['auth_bp', 'candidates_bp', 'jobs_bp']
```

---

## 🧪 ЛОКАЛЬНОЕ ТЕСТИРОВАНИЕ

```bash
# 1. Проверить импорты
cd backend
python -c "from app.routes import auth_bp, candidates_bp, jobs_bp; print('✓ All imports OK')"

# 2. Запустить тесты
python -m pytest tests/ -v --tb=short

# 3. Результат должен быть ≥ 80% PASSED
```

---

## 📋 GIT КОММИТ

```bash
git add backend/app/routes/auth.py
git add backend/app/routes/candidates.py
git add backend/app/routes/jobs.py
git add backend/app/routes/__init__.py
git commit -m "feat: implement all API blueprint modules - auth, candidates, jobs CRUD endpoints"
git push origin main
```

---

## ✅ ФИНАЛЬНЫЙ ЧЕКЛИСТ

- [ ] Три файла созданы (auth.py, candidates.py, jobs.py)
- [ ] __init__.py обновлен
- [ ] Python синтаксис валиден (компилируется)
- [ ] Импорты работают
- [ ] Тесты проходят ≥ 80%
- [ ] Git коммит сделан
- [ ] GitHub Actions прошел успешно
- [ ] Endpoints отвечают локально

---

## ⏱️ ВРЕМЕННАЯ ШКАЛА

```
14:00 - 14:30: Создание файлов
14:30 - 15:00: Локальное тестирование
15:00 - 15:30: CI/CD проверка
15:30 - 16:00: Финальные проверки
16:00: BACKEND 100% READY ✓
```

---

**НАЧНИ ПРЯМО СЕЙЧАС! У ТЕ ЕСТЬ 3+ ЧАСА ЗАПАСА ПЕРЕД DEADLINE! 💪**
