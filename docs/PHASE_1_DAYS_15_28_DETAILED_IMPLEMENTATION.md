# 🚀 Этап 1: Дни 15-28 - Детальная пошаговая реализация

## Обзор
Дни 15-28 фокусируются на расширении функциональности резюме, добавлении аналитики и оптимизации бэкенда.

---

## ДЕНЬ 15: API для парсинга и хранения резюме

### ШАГ 1: Создать API endpoints для резюме
**Путь:** `app/routes.py`

```python
from flask import Blueprint, request, jsonify
from app.models import Resume
from app import db

resume_bp = Blueprint('resume', __name__, url_prefix='/api/resumes')

# GET все резюме
@resume_bp.route('', methods=['GET'])
def get_resumes():
    resumes = Resume.query.all()
    return jsonify([r.to_dict() for r in resumes])

# POST новое резюме
@resume_bp.route('', methods=['POST'])
def create_resume():
    data = request.json
    resume = Resume(
        candidate_id=data.get('candidate_id'),
        parsed_data=data.get('parsed_data'),
        file_path=data.get('file_path')
    )
    db.session.add(resume)
    db.session.commit()
    return jsonify(resume.to_dict()), 201

# GET одно резюме
@resume_bp.route('/<int:resume_id>', methods=['GET'])
def get_resume(resume_id):
    resume = Resume.query.get_or_404(resume_id)
    return jsonify(resume.to_dict())

# DELETE резюме
@resume_bp.route('/<int:resume_id>', methods=['DELETE'])
def delete_resume(resume_id):
    resume = Resume.query.get_or_404(resume_id)
    db.session.delete(resume)
    db.session.commit()
    return '', 204
```

### ШАГ 2: Создать модель Resume
**Путь:** `app/models.py`

Добавить в существующий файл:

```python
class Resume(db.Model):
    __tablename__ = 'resumes'
    
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), nullable=False)
    file_path = db.Column(db.String(255), nullable=True)
    parsed_data = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    candidate = db.relationship('Candidate', backref='resumes')
    
    def to_dict(self):
        return {
            'id': self.id,
            'candidate_id': self.candidate_id,
            'file_path': self.file_path,
            'parsed_data': self.parsed_data,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
```

---

## ДЕНЬ 16: Парсинг PDF резюме с помощью pdfplumber

### ШАГ 1: Установить зависимости

```bash
pip install pdfplumber python-magic
```

### ШАГ 2: Создать сервис парсинга
**Путь:** `services/resume_parser.py`

```python
import pdfplumber
import os
from datetime import datetime

class ResumeParser:
    @staticmethod
    def extract_text_from_pdf(file_path):
        """Извлечь текст из PDF"""
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    
    @staticmethod
    def parse_resume(file_path):
        """Парсить резюме и извлечь структурированные данные"""
        text = ResumeParser.extract_text_from_pdf(file_path)
        
        parsed_data = {
            'raw_text': text,
            'skills': ResumeParser.extract_skills(text),
            'experience': ResumeParser.extract_experience(text),
            'education': ResumeParser.extract_education(text),
            'contacts': ResumeParser.extract_contacts(text)
        }
        
        return parsed_data
    
    @staticmethod
    def extract_skills(text):
        """Извлечь навыки из текста"""
        # Простая реализация - поиск по ключевым словам
        skills = []
        skill_keywords = ['Python', 'JavaScript', 'SQL', 'React', 'Django', 'AWS']
        
        for skill in skill_keywords:
            if skill.lower() in text.lower():
                skills.append(skill)
        
        return skills
    
    @staticmethod
    def extract_experience(text):
        """Извлечь опыт работы"""
        # Базовая реализация
        return {'raw_text': text[:500]}
    
    @staticmethod
    def extract_education(text):
        """Извлечь образование"""
        return {'raw_text': text[:300]}
    
    @staticmethod
    def extract_contacts(text):
        """Извлечь контакты"""
        import re
        emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text)
        phones = re.findall(r'\+?\d{1,3}[\s\-]?\d{1,14}', text)
        
        return {'emails': emails, 'phones': phones}
```

---

## ДЕНЬ 17: Интеграция парсинга в API

### ШАГ 1: Обновить API для загрузки файлов
**Путь:** `app/routes.py`

Добавить новый endpoint:

```python
import os
from werkzeug.utils import secure_filename
from services.resume_parser import ResumeParser

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
UPLOAD_FOLDER = 'uploads/resumes'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@resume_bp.route('/upload', methods=['POST'])
def upload_resume():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    candidate_id = request.form.get('candidate_id')
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    
    # Сохранить файл
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)
    
    # Парсить резюме
    try:
        parsed_data = ResumeParser.parse_resume(file_path)
    except Exception as e:
        return jsonify({'error': f'Failed to parse resume: {str(e)}'}), 400
    
    # Сохранить в БД
    resume = Resume(
        candidate_id=candidate_id,
        file_path=file_path,
        parsed_data=parsed_data
    )
    db.session.add(resume)
    db.session.commit()
    
    return jsonify(resume.to_dict()), 201
```

---

## ДЕНЬ 18-20: Фронтенд интеграция и улучшения UI

### Чекпоинт: Резюме система полностью интегрирована
- ✅ API endpoints работают
- ✅ Парсинг PDF функционирует
- ✅ Фронтенд компоненты отображают резюме
- ✅ Файлы загружаются и сохраняются

---

## ДЕНЬ 21-28: Аналитика и оптимизация

### ШАГ 1: Добавить аналитику
### ШАГ 2: Оптимизировать производительность  
### ШАГ 3: Развертывание на продакшене

---

## Контрольный список
- [ ] API endpoints для резюме созданы
- [ ] Модель Resume в БД
- [ ] Парсер резюме работает
- [ ] Фронтенд компоненты интегрированы
- [ ] Тестирование завершено
- [ ] Код задеплоен в продакшене
