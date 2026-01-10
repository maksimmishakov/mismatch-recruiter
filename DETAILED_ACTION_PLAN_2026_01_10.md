# 🎯 ПОЛНЫЙ АНАЛИЗ + ПОШАГОВЫЙ ПЛАН ДЕЙСТВИЙ
**Дата:** 10 января 2026, 14:25 MSK  
**Автор:** AI Assistant  
**Статус:** КРИТИЧНО - 52 GitHub Actions failures  
**Deadline:** 14 января, 14:00 MSK  
**ETA к готовности:** 4-5 часов

---

## 📊 ТЕКУЩИЙ СТАТУС ПРОЕКТА

### 🔴 GitHub Actions: ALL FAILING (52 errors)

```
❌ Backend Tests - FAILED
❌ Backend Tests & Build - FAILED
❌ CI/CD Pipeline - FAILED
❌ Frontend Tests - FAILED

Root Cause:
ModuleNotFoundError: No module named 'app.routes.auth'
```

### ✅ Что ты сделал правильно

| Компонент | Статус | Деталь |
|-----------|--------|--------|
| User Model | ✅ Fixed | Добавлены `set_password()` и `check_password()` с bcrypt |
| Health Endpoint | ✅ Fixed | Изменён на `/api/health`, правильный JSON ответ |
| Auth Логика | ✅ Implemented | Полная реализация в коммите 4d2d4a0 |
| Type Hints | ✅ Added | Все функции типизированы |
| Git History | ✅ Clean | Понятные коммит сообщения |
| Security | ✅ Good | Правильное хеширование паролей |

### ❌ Что ломает build

```python
# conftest.py пытается импортировать:
from app.routes.auth import auth_bp
from app.routes.candidates import candidates_bp
from app.routes.jobs import jobs_bp

# НО эти файлы НЕ СУЩЕСТВУЮТ в backend/app/routes/!
# Вероятно они:
# 1. В другой директории (app/api/)
# 2. Не закоммичены
# 3. Имеют другие имена
```

---

## 🔧 ИНСТРУКЦИЯ: 4 КРИТИЧЕСКИХ ШАГА

### ШАГ 1: ДИАГНОСТИКА (10 мин)

```bash
# Вход в проект
cd ~/mismatch-recruiter

# Найти файлы
find . -name "auth.py" -o -name "candidates.py" -o -name "jobs.py" | grep -v __pycache__

# Проверить структуру routes
ls -la backend/app/routes/

# Проверить конфтест
head -30 backend/tests/conftest.py

# Проверить регистрацию blueprints
grep -A 5 "register_blueprint" backend/app/__init__.py
```

**Возможные результаты:**

| Результат | Действие |
|-----------|----------|
| Файлы в `app/api/` | → Переместить в `app/routes/` |
| Файлы отсутствуют везде | → Создать по плану ниже |
| Файлы в `app/routes/` но не закоммичены | → `git add` + `git commit` |
| `conftest.py` импортирует неправильно | → Исправить пути импорта |

---

### ШАГ 2: СОЗДАНИЕ ФАЙЛОВ (30 мин)

Если файлы действительно отсутствуют, создай их:

#### 2.1 backend/app/routes/auth.py

```python
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from sqlalchemy.exc import IntegrityError

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
    
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Email already exists'}), 409
    
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

#### 2.2 backend/app/routes/candidates.py

```python
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.candidate import Candidate
from sqlalchemy.exc import IntegrityError

candidates_bp = Blueprint('candidates', __name__, url_prefix='/api/candidates')

@candidates_bp.route('', methods=['GET'])
@jwt_required()
def list_candidates():
    """Получить список кандидатов"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    candidates = Candidate.query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'candidates': [
            {
                'id': c.id,
                'first_name': c.first_name,
                'last_name': c.last_name,
                'email': c.email,
                'skills': c.skills or [],
                'experience_years': c.experience_years
            }
            for c in candidates.items
        ],
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
    
    try:
        db.session.add(candidate)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Email already exists'}), 409
    
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

#### 2.3 backend/app/routes/jobs.py

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
        'jobs': [
            {
                'id': j.id,
                'title': j.title,
                'description': j.description,
                'location': j.location,
                'salary_min': j.salary_min,
                'salary_max': j.salary_max,
                'required_skills': j.required_skills or [],
                'experience_years_min': j.experience_years_min,
                'status': j.status
            }
            for j in jobs.items
        ],
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

#### 2.4 backend/app/routes/__init__.py

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

### ШАГ 3: РЕГИСТРАЦИЯ BLUEPRINTS (5 мин)

Проверь `backend/app/__init__.py`, там должно быть:

```python
from app.routes.auth import auth_bp
from app.routes.candidates import candidates_bp
from app.routes.jobs import jobs_bp

# В функции create_app():
app.register_blueprint(auth_bp)
app.register_blueprint(candidates_bp)
app.register_blueprint(jobs_bp)
```

Если нет — добавь это!

---

### ШАГ 4: ТЕСТИРОВАНИЕ И PUSH (25 мин)

```bash
cd ~/mismatch-recruiter/backend

# 1. Проверить импорты
python -c "from app.routes import auth_bp, candidates_bp, jobs_bp; print('✓ All imports OK')"

# 2. Запустить тесты
python -m pytest tests/ -v --tb=short

# 3. Ожидаемый результат: ≥ 80% PASSED

# 4. Git коммит
cd ..
git add backend/app/routes/auth.py
git add backend/app/routes/candidates.py
git add backend/app/routes/jobs.py
git add backend/app/routes/__init__.py
git commit -m "feat: implement all API blueprint modules - fix ModuleNotFoundError"
git push origin main

# 5. Проверить GitHub Actions
# https://github.com/maksimmishakov/mismatch-recruiter/actions
# Должны появиться зелёные галочки ✅
```

---

## 📈 ПРОВЕРОЧНЫЙ ЛИСТ

### Диагностика ✓
- [ ] Нашел где находятся файлы
- [ ] Проверил conftest.py
- [ ] Проверил регистрацию blueprints

### Создание/Ремонт ✓
- [ ] Создал/исправил auth.py
- [ ] Создал/исправил candidates.py
- [ ] Создал/исправил jobs.py
- [ ] Обновил routes/__init__.py
- [ ] Проверил регистрацию в app/__init__.py

### Тестирование ✓
- [ ] Импорты работают локально
- [ ] Pytest ≥ 80% PASSED
- [ ] Git push успешен
- [ ] GitHub Actions все зелёные

### Финализация ✓
- [ ] Все 52 ошибки исправлены
- [ ] Backend полностью готов
- [ ] Готов к demo 14 января

---

## ⏱️ ВРЕМЕННАЯ ШКАЛА

```
Сейчас: ~14:30 MSK
├─ 14:30-14:40: Диагностика (ШАГ 1)
├─ 14:40-15:10: Создание файлов (ШАГ 2)
├─ 15:10-15:15: Регистрация (ШАГ 3)
├─ 15:15-15:40: Тестирование (ШАГ 4)
└─ 15:40: ГОТОВО! ✅

Осталось до deadline: ~72 часа
Дебор: ~68+ часов
```

---

## 🎯 ДАЛЬШЕ (11-14 января)

### 11 января
- Alembic миграции БД
- Staging на Amvera

### 12-13 января
- Demo-данные (тестовые кандидаты, вакансии)
- End-to-end тестирование

### 14 января, 14:00 MSK
- 🎉 DEMO ДЛЯ LAMODA

---

**УСПЕХОВ! Ты близко к финишу! 💪**
