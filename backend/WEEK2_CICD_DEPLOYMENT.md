# НЕДЕЛЯ 2: CI/CD Pipeline & Deployment
## 11-17 января 2026 (25-30 часов)

### ДЕНЬ 4 (11 января): GitHub Actions Setup

#### ЗАДАЧА 4.1: Create CI/CD Workflow (4 часа)

**Файл:** `.github/workflows/ci.yml`

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: mismatch_test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python 3.12
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
    
    - name: Install dependencies
      run: |
        cd backend
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov flake8 black
    
    - name: Lint with flake8
      run: |
        cd backend
        flake8 app/ routes/ models/ --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 app/ routes/ models/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    
    - name: Check format with black
      run: |
        cd backend
        black --check app/ routes/ models/ || true
    
    - name: Run tests
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/mismatch_test
        FLASK_ENV: testing
      run: |
        cd backend
        pytest --cov=app --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./backend/coverage.xml
        flags: unittests
        name: codecov-umbrella

  security:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
    
    - name: Install bandit
      run: pip install bandit
    
    - name: Run security scan
      run: |
        cd backend
        bandit -r app/ routes/ models/ -f json -o bandit-report.json || true
        bandit -r app/ routes/ models/
```

**Требования к выполнению:**
- [ ] Создать `.github/workflows/ci.yml` файл
- [ ] Setup Python 3.12 environment
- [ ] Install pytest для unit tests
- [ ] Setup PostgreSQL service
- [ ] Run linting (flake8, black)
- [ ] Run unit tests с coverage
- [ ] Run security scan (bandit)
- [ ] Upload coverage report

**Проверка:**
```bash
# Локально проверить синтаксис
python -m yaml .github/workflows/ci.yml

# Commit и push - GitHub Actions должен запуститься
git add .github/workflows/ci.yml
git commit -m "ci: add GitHub Actions workflow"
git push origin main

# Проверить на GitHub Actions dashboard
```

**Результат:** ✅ GitHub Actions workflow создан и протестирован

---

#### ЗАДАЧА 4.2: Add Unit Tests (3 часа)

**Структура тестов:**
```
backend/
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # Fixtures
│   ├── test_models.py        # Model tests
│   ├── test_routes.py        # API endpoint tests
│   ├── test_validation.py    # Schema validation tests
│   └── test_services.py      # Business logic tests
```

**Файл:** `backend/tests/conftest.py`
```python
import pytest
from app import create_app, db

@pytest.fixture
def app():
    """Create app for testing"""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Test client"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """CLI runner"""
    return app.test_cli_runner()
```

**Файл:** `backend/tests/test_models.py`
```python
def test_candidate_creation(app):
    """Test creating a candidate"""
    from app.models import Candidate
    
    with app.app_context():
        candidate = Candidate(
            name="John Doe",
            email="john@example.com",
            skills=["Python", "Flask"]
        )
        db.session.add(candidate)
        db.session.commit()
        
        assert candidate.id is not None
        assert candidate.name == "John Doe"
```

**Требования:**
- [ ] Создать `tests/` директорию
- [ ] Написать fixtures в `conftest.py`
- [ ] Написать model tests (100% coverage)
- [ ] Написать API endpoint tests (80%+ coverage)
- [ ] Написать validation tests
- [ ] Достичь 80%+ code coverage

**Проверка:**
```bash
cd backend
pytest --cov=app --cov-report=html
# Открыть htmlcov/index.html для просмотра
```

**Результат:** ✅ Unit tests написаны с 80%+ coverage

---

### ДЕНЬ 5 (12 января): Docker Configuration

#### ЗАДАЧА 5.1: Create Dockerfiles (3 часа)

**Файл:** `backend/Dockerfile`
```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    postgresql-client \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
  CMD python -c "import requests; requests.get('http://localhost:5000/health')"

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "wsgi:app"]
```

**Файл:** `docker-compose.yml`
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: mismatch
      POSTGRES_PASSWORD: ${DB_PASSWORD:-postgres}
      POSTGRES_DB: mismatch
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U mismatch"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
    environment:
      DATABASE_URL: postgresql://mismatch:${DB_PASSWORD:-postgres}@postgres:5432/mismatch
      FLASK_ENV: production
      JWT_SECRET_KEY: ${JWT_SECRET_KEY}
    depends_on:
      postgres:
        condition: service_healthy
    volumes:
      - ./backend:/app
    command: python app.py

volumes:
  postgres_data:
```

**Требования:**
- [ ] Создать `backend/Dockerfile`
- [ ] Создать `docker-compose.yml` в root
- [ ] Добавить health checks
- [ ] Настроить environment variables
- [ ] Оптимизировать image size

**Проверка:**
```bash
# Build image
docker build -t mismatch-recruiter:latest ./backend

# Run with docker-compose
docker-compose up -d

# Check logs
docker-compose logs -f backend

# Test health
curl http://localhost:5000/health

# Stop
docker-compose down
```

**Результат:** ✅ Docker configuration готова

---

### ДЕНЬ 6 (13 января): Amvera Cloud Deployment

#### ЗАДАЧА 6.1: Setup Amvera Deployment (4 часа)

**Требования:**
- [ ] Аккаунт на Amvera Cloud
- [ ] Push Docker image
- [ ] Configure production environment
- [ ] Setup database (PostgreSQL)
- [ ] Configure domain & SSL
- [ ] Setup monitoring

**Инструкции:**
```bash
# 1. Login to Amvera
amvera login

# 2. Create application
amvera app:create mismatch-recruiter --region=eu

# 3. Build and push image
cd backend
docker build -t mismatch-recruiter:latest .
amvera image:push mismatch-recruiter:latest

# 4. Create production config
amvera env:set \\
  FLASK_ENV=production \\
  JWT_SECRET_KEY=$(python -c 'import secrets; print(secrets.token_urlsafe(32))') \\
  DATABASE_URL=postgresql://... \\
  CORS_ORIGINS=https://yourdomain.com \\
  SENTRY_DSN=https://...

# 5. Deploy
amvera deploy

# 6. Check status
amvera app:status
```

**Результат:** ✅ Application deployed to Amvera Cloud

---

### ДЕНЬ 7 (14 января): Testing & Optimization

#### ЗАДАЧА 7.1: Integration Tests & Performance (4 часа)

**Требования:**
- [ ] Write integration tests
- [ ] Performance benchmarking
- [ ] Load testing
- [ ] Optimize slow endpoints
- [ ] Final health check

**Итоги НЕДЕЛЯ 2:** ✅ Production deployment ready (95% → 97% готовности)
