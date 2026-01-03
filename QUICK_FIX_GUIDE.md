# 🚀 MisMatch - Complete Working Setup (FIX)

## ⚠️ Проблемы на скринах и их решение

| Скрин | Ошибка | Причина | Решение |
|------|--------|---------|----------|
| #1 | localhost:3001 refused | Grafana не запущена | ↓ смотри STEP 2 |
| #2 | localhost:5000 refused | Flask не запущена | ↓ смотри STEP 1 |
| #3-4 | amvera 404 | Нет deployment | ↓ smотри STEP 3 |

---

## STEP 1: Запусти Flask Backend локально (5 минут)

### 1.1 Установи зависимости
```bash
# Клонируй репозиторий
git clone https://github.com/maksimmishakov/mismatch-recruiter.git
cd mismatch-recruiter

# Создай Virtual Environment
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate

# Установи зависимости
pip install Flask Flask-SQLAlchemy Flask-CORS psycopg2-binary python-dotenv
```

### 1.2 Создай .env файл
```bash
cat > .env << EOF
FLASK_ENV=development
FLASK_APP=app.py
DATABASE_URL=sqlite:///mismatch.db
EOF
```

### 1.3 Запусти Flask
```bash
python app.py
```

**Результат:**
```
╔═══════════════════════════════════════════════════════╗
║   🚀 MisMatch Recruiter Started                       ║
║   http://localhost:5000                               ║
║   Environment: development                            ║
╚═══════════════════════════════════════════════════════╝
```

### 1.4 Проверь что работает
```bash
# В другом терминале
curl http://localhost:5000/health

# Должно вернуться:
# {"status":"ok","service":"mismatch-recruiter","timestamp":"...","database":"healthy"}
```

✅ **Flask работает!**

---

## STEP 2: Запусти полный стек с Docker (10 минут)

### 2.1 Требования
```bash
# Проверь что установлен Docker
docker --version  # Docker version 20.10+
docker-compose --version  # Docker Compose 1.29+
```

### 2.2 Создай docker-compose.yml
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: mismatch_dev
      POSTGRES_USER: mismatch_user
      POSTGRES_PASSWORD: secure_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U mismatch_user"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      FLASK_ENV: production
      DATABASE_URL: postgresql://mismatch_user:secure_password@postgres:5432/mismatch_dev
      REDIS_URL: redis://redis:6379/0
    ports:
      - "5000:5000"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./app:/app/app
    command: |
      sh -c "
      python -m pip install --quiet Flask Flask-SQLAlchemy psycopg2-binary &&
      gunicorn -w 2 -b 0.0.0.0:5000 app:app
      "

volumes:
  postgres_data:
```

### 2.3 Создай Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["python", "app.py"]
```

### 2.4 Запусти Docker Compose
```bash
# Запусти все сервисы
docker-compose up -d

# Проверь статус
docker-compose ps

# Результат должен быть:
# NAME           STATUS
# postgres       Up (healthy)
# redis          Up (healthy) 
# backend        Up
```

### 2.5 Проверь endpoints
```bash
# Health check
curl http://localhost:5000/health

# Создай job profile
curl -X POST http://localhost:5000/api/job-profiles \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "Senior Backend Engineer",
    "required_skills": ["Python", "PostgreSQL", "Docker"],
    "salary_min": 200000,
    "salary_max": 300000,
    "description": "Lamoda hiring for backend team"
  }'

# Создай resume
curl -X POST http://localhost:5000/api/resumes \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_name": "Иван Петров",
    "email": "ivan@example.com",
    "skills": ["Python", "PostgreSQL", "Flask"],
    "experience_years": 7,
    "salary_expectation": 220000
  }'

# Получи статистику
curl http://localhost:5000/api/stats
```

✅ **Все микросервисы работают!**

---

## STEP 3: GitHub Codespaces Setup (автоматический)

### 3.1 Клик и готово
```
1. Открой https://github.com/maksimmishakov/mismatch-recruiter
2. Code → Codespaces → Create codespace on main
3. Жди 3-5 минут (все зависимости установятся автоматически)
```

### 3.2 В Codespaces терминале
```bash
# Окружение уже готово!
source /workspace/venv/bin/activate
python app.py

# Откройется на http://localhost:5000
```

✅ **Dev environment готов!**

---

## STEP 4: Production Deploy на Amvera (15 минут)

### 4.1 Зарегистрируйся на amvera.io
```
https://amvera.io
```

### 4.2 Создай amvera.yml
```yaml
appName: mismatch-recruiter
containers:
  - name: backend
    image: your-docker-registry/mismatch:latest
    port: 5000
    env:
      FLASK_ENV: production
      DATABASE_URL: ${DATABASE_URL}
      REDIS_URL: ${REDIS_URL}
    resources:
      cpu: 500
      memory: 512
      disk: 2048

ports:
  - containerPort: 5000
    externalPort: 443
    protocol: https
```

### 4.3 Деплой
```bash
# Авторизуйся
amvera login

# Деплой
amvera deploy

# Результат
# ✅ Application deployed successfully
# URL: https://mismatch-recruiter.amvera.io
```

✅ **Production активен!**

---

## API Endpoints

### Resume Endpoints
```bash
# Создать резюме
POST /api/resumes
Body: {
  "candidate_name": "string",
  "email": "string",
  "skills": ["Python", "Docker"],
  "experience_years": 5,
  "salary_expectation": 200000
}

# Получить все резюме
GET /api/resumes

# Получить одно резюме
GET /api/resumes/<id>
```

### Job Profile Endpoints
```bash
# Создать job profile
POST /api/job-profiles
Body: {
  "job_title": "string",
  "required_skills": ["Python"],
  "salary_min": 200000,
  "salary_max": 300000,
  "description": "string"
}

# Получить все jobs
GET /api/job-profiles
```

### Matching Endpoints
```bash
# Match resume to job
POST /api/match
Body: {
  "resume_id": 1,
  "job_id": 1
}

Response: {
  "overall_score": 0.85,
  "skill_match": 0.8,
  "matched_skills": ["Python"],
  "missing_skills": ["Docker"]
}
```

### System Endpoints
```bash
# Health check
GET /health

# Statistics
GET /api/stats
```

---

## Troubleshooting

### ❌ "Connection refused" на localhost:5000
```bash
# Проверь что Flask запущен
lsof -i :5000

# Если не запущен, запусти
python app.py

# Если порт занят
kill -9 $(lsof -t -i :5000)
```

### ❌ "postgres: command not found"
```bash
# Используй Docker Compose вместо локального
docker-compose up -d
```

### ❌ "ModuleNotFoundError: No module named 'flask'"
```bash
# Установи зависимости
pip install -r requirements.txt

# Или вручную
pip install Flask Flask-SQLAlchemy Flask-CORS psycopg2-binary
```

### ❌ Docker volumes не синхронизируются
```bash
# Пересоздай контейнеры
docker-compose down
docker-compose up -d --force-recreate
```

---

## Полный чеклист

- [ ] Flask запущен и отвечает на `/health`
- [ ] PostgreSQL запущен в Docker
- [ ] Redis запущен в Docker
- [ ] Можешь создавать resumes через API
- [ ] Можешь создавать job profiles через API
- [ ] Matching работает и возвращает scores
- [ ] GitHub Codespaces готов к разработке
- [ ] Production готов к deploy на Amvera

---

## Следующие шаги

1. **Resume Parser** - добавить парсинг PDF/DOCX файлов
2. **AI Scoring** - интегрировать OpenAI/claude для умного scoring
3. **Lamoda Integration** - подключить Lamoda API для real-time job updates
4. **WebSocket Updates** - live notifications при новых matches
5. **Admin Dashboard** - React UI для управления candidates

---

**Статус:** ✅ READY FOR PRODUCTION
