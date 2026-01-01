# MisMatch Recruitment Platform - Deployment & Testing Guide

## Phase 1: Testing & Quality Assurance (Days 15-28)

### Unit Testing Setup

**Backend Tests - tests/test_routes.py:**
```python
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'

def test_get_candidates(client):
    response = client.get('/api/candidates')
    assert response.status_code == 200
    assert 'candidates' in response.json
```

**Frontend Tests - frontend/src/__tests__/Dashboard.test.tsx:**
```typescript
import { render, screen } from '@testing-library/react';
import { Dashboard } from '../components/Dashboard';

test('renders dashboard component', () => {
  render(<Dashboard />);
  expect(screen.getByText(/Matches/i)).toBeInTheDocument();
});
```

### Integration Testing

**Test API Integration:**
```bash
# Start backend
python app.py

# In another terminal, run integration tests
curl http://localhost:5000/api/health
curl http://localhost:5000/api/candidates
curl http://localhost:5000/api/matches?user_id=test123
```

### Performance Testing

**Load Testing with Locust:**
```python
from locust import HttpUser, task, between

class APIUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def health_check(self):
        self.client.get('/api/health')

    @task
    def get_matches(self):
        self.client.get('/api/matches?user_id=test')
```

## Phase 2: Deployment (Days 20-28)

### Development Environment

**Requirements - requirements.txt:**
```
Flask==2.3.0
flask-cors==4.0.0
python-dotenv==1.0.0
psycopg2-binary==2.9.6
Gunicorn==20.1.0
pytest==7.3.0
```

### Production Deployment

**Docker Configuration - Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

**Docker Compose - docker-compose.yml:**
```yaml
version: '3.8'
services:
  backend:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mismatch
    depends_on:
      - db
  
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=mismatch
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### CI/CD Pipeline

**.github/workflows/deploy.yml:**
```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest
  
  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to production
        run: |
          echo "Deploying application..."
          # Add your deployment commands here
```

## Testing Checklist

- [ ] Unit tests passing (backend)
- [ ] Component tests passing (frontend)
- [ ] API integration tests successful
- [ ] CORS headers correct
- [ ] Error handling working
- [ ] Performance benchmarks met
- [ ] Security checks passed
- [ ] Database migrations applied
- [ ] Environment variables configured
- [ ] Docker containers building successfully
- [ ] CI/CD pipeline operational
- [ ] Load testing shows acceptable response times
- [ ] SSL/TLS certificates configured
- [ ] Monitoring and logging enabled
- [ ] Backup procedures documented

## Monitoring & Logging

**Application Logging:**
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

## Troubleshooting Common Issues

### CORS Errors
- Verify frontend URL in CORS configuration
- Check browser developer console for error details
- Ensure proper Content-Type headers are set

### Database Connection Errors
- Verify DATABASE_URL environment variable
- Check database server is running
- Confirm database credentials

### Performance Issues
- Add database indexes for frequently queried columns
- Implement caching strategy
- Use connection pooling
- Profile API response times

## Success Criteria

All tests passing before deployment to production:
- Backend: >90% code coverage
- Frontend: >85% component coverage
- API response time: <200ms for 95th percentile
- System availability: >99.5% uptime
