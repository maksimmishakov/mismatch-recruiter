# 🚀 ПОЛНЫЙ ПЛАН РАЗВИТИЯ MISMATCH RECRUITER - ЭТАПЫ 2-4
## Супер Детальное Руководство с Кодом (Неделя 3-6)

### 📋 СОДЕРЖАНИЕ
1. **ЭТАП 2: AI MATCHING ALGORITHM (Неделя 3-4)** - Machine Learning для матчинга
2. **ЭТАП 3: FRONTEND (Неделя 4-5)** - React приложение с UI
3. **ЭТАП 4: ADVANCED FEATURES (Неделя 5-6)** - Email, scheduling, analytics, Celery
4. **Полный Технический Стек и Best Practices**

---

## 🧠 ЭТАП 2: AI MATCHING ALGORITHM (Неделя 3-4)

### Цель
Реализовать интеллектуальное сопоставление кандидатов и вакансий с использованием ML

### Архитектура ML Pipeline
```
Входные данные:
  ├─ Кандидат: skills, experience, location, education
  └─ Вакансия: required_skills, experience_years, location, salary

         ↓
    
    ML Pipeline:
      ├─ Text Preprocessing (извлечение ключевых слов)
      ├─ Feature Vectorization (TF-IDF, embeddings)
      ├─ Similarity Calculation (cosine similarity)
      └─ Weight Application (skills: 40%, exp: 30%, loc: 15%, sal: 10%, text: 5%)

         ↓

    Match Score: 0.0 - 1.0 (0-100%)
    Quality: EXCELLENT (85%+), GOOD (70%+), FAIR (50%+), POOR (30%+), UNSUITABLE
```

### ШАГ 1: Установить ML библиотеки

**Обновить requirements.txt:**

```txt
Flask>=3.0.0
Flask-SQLAlchemy>=3.1.1
Flask-CORS>=4.0.0
Flask-JWT-Extended>=4.6.0
Flask-Migrate>=4.0.5
SQLAlchemy>=2.0.0
psycopg2-binary>=2.9.9
Redis>=5.0.0
gunicorn>=21.2.0
python-dotenv>=1.0.0
requests>=2.31.0
pydantic>=2.5.0
PyPDF2>=2.6.0
python-docx>=0.8.11
celery>=5.3.4
raven>=6.10.0
sentry-sdk>=1.38.0
graphene>=3.3.0
graphene-sqlalchemy>=3.1.0

# 🆕 ML LIBRARIES
scikit-learn>=1.3.0
numpy>=1.24.0
pandas>=2.0.0
nltk>=3.8.0
spacy>=3.7.0

# Optional: Deep Learning
# transformers>=4.30.0  # BERT, RoBERTa
# torch>=2.0.0  # PyTorch
```

**Выполнить:**
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### ШАГ 2: Создать ML модель (app/ml/matcher.py)

**Полный файл с MatchingEngine:**

```python
# app/ml/matcher.py
"""
Machine Learning Matching Engine
Сопоставляет кандидатов и вакансии на основе ML

Использует:
- TF-IDF для текстовой схожести
- Custom weights для разных критериев
- Cosine similarity для scoring
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import logging

logger = logging.getLogger(__name__)

# Download NLTK data (run once)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')


class MatchingEngine:
    """
    ML Engine для сопоставления кандидатов и вакансий
    """
    
    def __init__(self):
        """Инициализация engine"""
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=100,
            stop_words='english',
            lowercase=True,
            min_df=1
        )
        self.stop_words = set(stopwords.words('english'))
        
    def preprocess_text(self, text):
        """Предварительная обработка текста"""
        if not text:
            return ""
        
        text = text.lower()
        tokens = word_tokenize(text)
        tokens = [
            token for token in tokens
            if token not in string.punctuation 
            and token not in self.stop_words
        ]
        return ' '.join(tokens)
    
    def extract_skills(self, text):
        """Извлечение навыков из текста"""
        KNOWN_SKILLS = {
            'python', 'javascript', 'java', 'c++', 'ruby', 'go', 'rust',
            'typescript', 'sql', 'html', 'css', 'react', 'vue', 'angular',
            'django', 'flask', 'fastapi', 'nodejs', 'express',
            'mongodb', 'postgresql', 'mysql', 'redis', 'elasticsearch',
            'docker', 'kubernetes', 'aws', 'gcp', 'azure', 'jenkins',
            'git', 'rest api', 'graphql', 'microservices', 'devops'
        }
        
        text_lower = text.lower()
        return [s for s in KNOWN_SKILLS if s in text_lower]
    
    def calculate_text_similarity(self, candidate_text, job_text):
        """Вычислить косинусное сходство"""
        try:
            candidate_clean = self.preprocess_text(candidate_text)
            job_clean = self.preprocess_text(job_text)
            
            if not candidate_clean or not job_clean:
                return 0.0
            
            texts = [candidate_clean, job_clean]
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(texts)
            similarity = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]
            
            return float(similarity)
            
        except Exception as e:
            logger.error(f"Error calculating text similarity: {e}")
            return 0.0
    
    def calculate_skills_match(self, candidate_skills, required_skills):
        """Вычислить процент совпадения навыков"""
        if not required_skills:
            return 1.0
        
        candidate_set = set([s.lower() for s in candidate_skills])
        required_set = set([s.lower() for s in required_skills])
        matching = candidate_set & required_set
        
        return float(len(matching) / len(required_set))
    
    def calculate_experience_match(self, candidate_years, required_years):
        """Вычислить совпадение по опыту"""
        if not required_years or required_years == 0:
            return 1.0
        
        if candidate_years >= required_years:
            return 1.0
        
        return float(min(candidate_years / required_years, 1.0))
    
    def calculate_location_match(self, candidate_location, job_location, remote=False):
        """Вычислить совпадение по локации"""
        if not job_location:
            return 1.0
        
        if remote or candidate_location.lower() == job_location.lower():
            return 1.0
        
        return 0.5
    
    def calculate_salary_fit(self, candidate_salary_expectation, offered_salary):
        """Вычислить совпадение по зарплате"""
        if not offered_salary or not candidate_salary_expectation:
            return 0.8
        
        if offered_salary >= candidate_salary_expectation:
            return 1.0
        
        coverage = offered_salary / candidate_salary_expectation
        
        if coverage < 0.7:
            return coverage * 0.7
        
        return float(coverage)
    
    def calculate_match_score(self, candidate, job, weights=None):
        """Вычислить общий match score"""
        if weights is None:
            weights = {
                'skills': 0.40,
                'experience': 0.30,
                'location': 0.15,
                'salary': 0.10,
                'text_similarity': 0.05
            }
        
        try:
            candidate_skills = candidate.get('skills', [])
            required_skills = job.get('required_skills', [])
            skills_score = self.calculate_skills_match(candidate_skills, required_skills)
            
            candidate_exp = candidate.get('experience_years', 0)
            required_exp = job.get('required_experience', 0)
            experience_score = self.calculate_experience_match(candidate_exp, required_exp)
            
            candidate_location = candidate.get('location', '')
            job_location = job.get('location', '')
            job_remote = job.get('remote', False)
            location_score = self.calculate_location_match(
                candidate_location, job_location, job_remote
            )
            
            candidate_salary = candidate.get('salary_expectation', 0)
            job_salary = job.get('salary', 0)
            salary_score = self.calculate_salary_fit(candidate_salary, job_salary)
            
            candidate_text = candidate.get('resume_text', '')
            job_text = job.get('description', '')
            text_similarity = self.calculate_text_similarity(candidate_text, job_text)
            
            overall_score = (
                skills_score * weights['skills'] +
                experience_score * weights['experience'] +
                location_score * weights['location'] +
                salary_score * weights['salary'] +
                text_similarity * weights['text_similarity']
            )
            
            return {
                'overall_score': float(overall_score),
                'score_percentage': float(overall_score * 100),
                'breakdown': {
                    'skills': float(skills_score),
                    'experience': float(experience_score),
                    'location': float(location_score),
                    'salary': float(salary_score),
                    'text_similarity': float(text_similarity)
                },
                'match_quality': self._determine_quality(overall_score)
            }
            
        except Exception as e:
            logger.error(f"Error calculating match score: {e}")
            return {'overall_score': 0.0, 'error': str(e)}
    
    def _determine_quality(self, score):
        """Определить качество матча"""
        if score >= 0.85:
            return 'EXCELLENT'
        elif score >= 0.70:
            return 'GOOD'
        elif score >= 0.50:
            return 'FAIR'
        elif score >= 0.30:
            return 'POOR'
        else:
            return 'UNSUITABLE'


_matcher = None

def get_matcher():
    """Получить singleton instance"""
    global _matcher
    if _matcher is None:
        _matcher = MatchingEngine()
    return _matcher
```

---

## 🎨 ЭТАП 3: FRONTEND (Неделя 4-5)

### React структура

```
frontend/
├── src/
│   ├── components/
│   │   ├── Dashboard/
│   │   ├── Candidates/
│   │   ├── Jobs/
│   │   ├── Matches/
│   │   ├── Analytics/
│   │   └── Common/
│   ├── pages/
│   ├── hooks/
│   ├── services/
│   ├── App.jsx
│   └── index.js
├── public/
└── package.json
```

### Инициализация

```bash
npx create-react-app frontend
cd frontend
npm install axios react-router-dom zustand
npm install -D tailwindcss
```

### Ключевые компоненты

1. **CandidateList.jsx** - список кандидатов с поиском
2. **JobList.jsx** - список вакансий
3. **MatchCard.jsx** - карточка матча с ML scores
4. **MatchScore.jsx** - визуализация scores (pie chart)
5. **Analytics.jsx** - dashboard (уже существует)

---

## ⚡ ЭТАП 4: ADVANCED FEATURES (Неделя 5-6)

### 1. Email с Celery

```python
# app/tasks.py

from celery import shared_task
from flask_mail import Message

@shared_task
def send_match_notification(candidate_id, job_id, score):
    """Отправить уведомление о матче"""
    try:
        # Получить данные
        candidate = Candidate.query.get(candidate_id)
        job = Job.query.get(job_id)
        
        # Сформировать email
        msg = Message(
            subject=f"Perfect Match: {job.title}",
            recipients=[candidate.email],
            html=f"""<h2>Great Match Found!</h2>
                     <p>Score: {int(score * 100)}%</p>
                     <p>{job.description}</p>"""
        )
        
        mail.send(msg)
        return True
    except Exception as e:
        logger.error(f"Error: {e}")
        return False
```

### 2. Interview Scheduling

```python
# app/models.py
class Interview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'))
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    scheduled_at = db.Column(db.DateTime)
    interview_type = db.Column(db.String(50))  # PHONE, VIDEO, IN_PERSON
    status = db.Column(db.String(50), default='SCHEDULED')
    feedback = db.Column(db.Text)
    rating = db.Column(db.Integer)  # 1-5
```

### 3. Analytics API

```python
# app/routes/analytics.py

@analytics_bp.route('/overview')
def get_overview():
    """Статистика платформы"""
    return jsonify({
        'candidates': Candidate.query.count(),
        'jobs': Job.query.count(),
        'matches': Match.query.count(),
        'good_matches': Match.query.filter(
            Match.overall_score >= 0.7
        ).count(),
        'average_score': db.session.query(
            func.avg(Match.overall_score)
        ).scalar()
    })
```

---

## 📊 TESTING ENDPOINTS

### Тестирование ML Scoring

```bash
# Вычислить score между кандидатом и вакансией
curl -X POST http://localhost:5000/api/matches/calculate_score \
  -H "Content-Type: application/json" \
  -d '{
    "candidate": {
      "skills": ["Python", "Django"],
      "experience_years": 5,
      "location": "Moscow",
      "resume_text": "Senior Python Developer",
      "salary_expectation": 150000
    },
    "job": {
      "title": "Backend Developer",
      "description": "Looking for Python expert",
      "required_skills": ["Python", "Django"],
      "required_experience": 3,
      "location": "Moscow",
      "remote": false,
      "salary": 180000
    }
  }'

# Найти лучших кандидатов для вакансии
curl http://localhost:5000/api/matches/find_best_matches/1?limit=10&min_score=0.5

# Найти лучшие вакансии для кандидата
curl http://localhost:5000/api/matches/find_best_jobs/1?limit=10&min_score=0.5
```

---

## 🚀 DEPLOYMENT CHECKLIST

### Phase 2 (ML)
- [x] Установить зависимости
- [x] Создать MatchingEngine
- [x] Реализовать scoring algorithm
- [x] Создать API endpoints
- [x] Добавить в БД
- [x] Тестирование
- [ ] Deploy на Amvera

### Phase 3 (Frontend)
- [ ] React проект
- [ ] Компоненты
- [ ] API integration
- [ ] Authentication
- [ ] Deploy (Netlify/Vercel)

### Phase 4 (Advanced)
- [ ] Celery + Redis
- [ ] Email notifications
- [ ] Interview scheduling
- [ ] Analytics
- [ ] Testing
- [ ] Final deploy

---

## 💡 QUICK LINKS

- [Scikit-learn Documentation](https://scikit-learn.org/)
- [Flask-Celery Integration](https://flask.palletsprojects.com/)
- [React Best Practices](https://reactjs.org/)
- [NLTK Tutorial](https://www.nltk.org/)

---

**Последнее обновление:** 15 января 2026 г.
**Статус:** ✅ READY FOR IMPLEMENTATION
