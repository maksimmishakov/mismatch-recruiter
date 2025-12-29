# Testing Guide

## Overview
Comprehensive testing strategy and guidelines for the MisMatch Recruitment Bot.

## Testing Levels

### 1. Unit Tests
Test individual functions and methods in isolation.

**Framework**: pytest
**Coverage Target**: 85%+

```bash
# Run all unit tests
pytest tests/unit/ -v

# Run with coverage
pytest --cov=app tests/ --cov-report=html
```

### 2. Integration Tests
Test interactions between multiple components.

```bash
# Run integration tests
pytest tests/integration/ -v

# Run with database
pytest tests/integration/ --db postgresql
```

### 3. End-to-End Tests
Test complete workflows from API to database.

```bash
# Run E2E tests
pytest tests/e2e/ -v
```

## Unit Test Examples

### Test Interview Question Generation

```python
import pytest
from app.services.interview_generator import InterviewGenerator
from unittest.mock import patch, MagicMock

@pytest.fixture
def generator():
    return InterviewGenerator()

@pytest.mark.asyncio
async def test_generate_questions(generator):
    """Test question generation with valid input"""
    job_description = "Senior Python Developer"
    candidate_profile = "John - 5 years Python"
    
    with patch('app.services.interview_generator.openai.ChatCompletion.create') as mock_openai:
        mock_openai.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content=json.dumps([
                {"question": "Describe your Python experience"},
                {"question": "What is async/await?"}
            ])))]
        )
        
        result = await generator.generate(
            job_description=job_description,
            candidate_profile=candidate_profile,
            num_questions=2
        )
        
        assert len(result['questions']) == 2
        assert result['model'] == 'gpt-4o-mini'
        mock_openai.assert_called_once()

@pytest.mark.asyncio
async def test_generate_questions_invalid_input(generator):
    """Test question generation with invalid input"""
    with pytest.raises(ValueError):
        await generator.generate(
            job_description="",  # Empty
            candidate_profile="John"
        )
```

### Test Database Operations

```python
@pytest.fixture
def db_session(test_db):
    """Provide test database session"""
    return test_db.Session()

def test_create_candidate(db_session):
    """Test candidate creation"""
    candidate = Candidate(
        name="Jane Doe",
        email="jane@example.com",
        experience_years=4,
        skills=["Python", "FastAPI"]
    )
    db_session.add(candidate)
    db_session.commit()
    
    fetched = db_session.query(Candidate).filter_by(email="jane@example.com").first()
    assert fetched.name == "Jane Doe"
    assert fetched.experience_years == 4

def test_candidate_unique_email(db_session):
    """Test email uniqueness constraint"""
    candidate1 = Candidate(name="John", email="john@example.com")
    candidate2 = Candidate(name="Jane", email="john@example.com")
    
    db_session.add(candidate1)
    db_session.commit()
    
    db_session.add(candidate2)
    with pytest.raises(IntegrityError):
        db_session.commit()
```

### Test API Endpoints

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_generate_questions_endpoint():
    """Test interview questions endpoint"""
    payload = {
        "job_description": "Senior Python Developer",
        "candidate_profile": "John - 4 years Python",
        "num_questions": 5
    }
    
    response = client.post("/api/generate-interview-questions", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "questions" in data
    assert len(data["questions"]) == 5
    assert "generated_at" in data

def test_generate_questions_missing_field():
    """Test endpoint with missing required field"""
    payload = {
        "job_description": "Senior Python Developer"
        # Missing candidate_profile
    }
    
    response = client.post("/api/generate-interview-questions", json=payload)
    assert response.status_code == 422  # Validation error

def test_evaluate_candidate_endpoint():
    """Test candidate evaluation endpoint"""
    payload = {
        "candidate_id": "cand_123",
        "interview_id": "int_456",
        "responses": [
            {"question_id": 1, "response": "My Python experience includes..."},
            {"question_id": 2, "response": "Async/await allows..."},
        ]
    }
    
    response = client.post("/api/evaluate-candidate", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "evaluation_id" in data
    assert "scores" in data
    assert "feedback" in data
```

## Test Configuration

### pytest.ini

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --verbose
    --strict-markers
    --disable-warnings
    -ra
markers =
    asyncio: marks tests as async
    integration: marks tests as integration tests
    e2e: marks tests as end-to-end tests
```

### conftest.py

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import Base
from app.main import app

@pytest.fixture(scope="session")
def test_db():
    """Create test database"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine

@pytest.fixture
def test_db_session(test_db):
    """Provide test database session"""
    connection = test_db.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client():
    """Provide FastAPI test client"""
    return TestClient(app)
```

## Performance Testing

### Load Testing with Locust

```python
from locust import HttpUser, task, between

class RecruitmentBotUser(HttpUser):
    wait_time = between(1, 3)
    
    @task(3)
    def generate_questions(self):
        self.client.post("/api/generate-interview-questions", json={
            "job_description": "Senior Python Developer",
            "candidate_profile": "John - 5 years experience",
            "num_questions": 5
        })
    
    @task(1)
    def evaluate_candidate(self):
        self.client.post("/api/evaluate-candidate", json={
            "candidate_id": "cand_123",
            "interview_id": "int_456",
            "responses": [{"question_id": 1, "response": "Test response"}]
        })
    
    @task(1)
    def health_check(self):
        self.client.get("/health")
```

```bash
# Run load test
locust -f tests/load_test.py --host=http://localhost:8000
```

## Security Testing

### Test SQL Injection Prevention

```python
def test_sql_injection_prevention():
    """Test that SQL injection is prevented"""
    malicious_input = "'; DROP TABLE candidates; --"
    
    response = client.post("/api/generate-interview-questions", json={
        "job_description": malicious_input,
        "candidate_profile": "John"
    })
    
    # Should not execute malicious SQL
    assert response.status_code in [200, 400, 422]
    
    # Verify table still exists
    db_session.query(Candidate).count()  # Should not raise
```

### Test Authentication

```python
def test_missing_auth_token():
    """Test that missing auth token is rejected"""
    response = client.post("/api/generate-interview-questions", json={
        "job_description": "Senior Python Developer",
        "candidate_profile": "John"
    })
    assert response.status_code == 401

def test_invalid_auth_token():
    """Test that invalid token is rejected"""
    response = client.post(
        "/api/generate-interview-questions",
        json={...},
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401
```

## Continuous Integration

### GitHub Actions Workflow

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_PASSWORD: password
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      redis:
        image: redis:6
    
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run unit tests
        run: pytest tests/unit/ --cov=app
      
      - name: Run integration tests
        env:
          DATABASE_URL: postgresql://postgres:password@localhost:5432/Mismatch
          REDIS_URL: redis://localhost:6379
        run: pytest tests/integration/
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
```

## Test Coverage Goals

- **Overall**: 85%+
- **Business Logic**: 90%+
- **Routes**: 80%+
- **Database**: 75%+
- **Utilities**: 70%+

## Running Tests Locally

```bash
# All tests
pytest

# Specific file
pytest tests/unit/test_interview_generator.py

# Specific test
pytest tests/unit/test_interview_generator.py::test_generate_questions

# With coverage
pytest --cov=app --cov-report=html

# Parallel execution
pytest -n auto

# Only failed tests
pytest --lf

# With markers
pytest -m "not e2e"
```

## Test Best Practices

1. **Use Fixtures**: Reuse setup code with pytest fixtures
2. **Mock External Dependencies**: Use unittest.mock for external services
3. **Test One Thing**: Each test should verify one behavior
4. **Clear Names**: Test names should describe what they test
5. **Arrange-Act-Assert**: Follow AAA pattern
6. **No Test Dependencies**: Tests should be independent
7. **Deterministic**: Tests should always produce the same result
8. **Fast**: Unit tests should be fast

## Debugging Tests

```bash
# Run with print statements
pytest -s

# Drop into debugger on failure
pytest --pdb

# Verbose output
pytest -vv

# Show local variables
pytest -l
```

## Coverage Reports

```bash
# Generate HTML report
pytest --cov=app --cov-report=html

# View coverage
open htmlcov/index.html
```

## Troubleshooting

### Database Lock Errors
- Use in-memory SQLite for tests
- Use transaction rollback for cleanup

### Async Test Failures
- Use `@pytest.mark.asyncio` decorator
- Use `pytest-asyncio` plugin

### Mock Issues
- Verify patch paths are correct
- Check mock was called with `assert_called()`

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/advanced/testing-dependencies/)
- [SQLAlchemy Testing](https://docs.sqlalchemy.org/en/20/faq/testing.html)
- [Locust Load Testing](https://locust.io/)
