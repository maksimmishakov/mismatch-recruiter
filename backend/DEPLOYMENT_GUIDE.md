# MisMatch Recruiter - Deployment Guide

## Prerequisites
- Docker & Docker Compose installed
- PostgreSQL 15+ (if not using Docker)
- Python 3.11+
- Node.js 18+
- Git

## Local Development Setup

### 1. Clone Repository
```bash
git clone https://github.com/maksimmishakov/mismatch-recruiter.git
cd mismatch-recruiter
```

### 2. Using Docker Compose (Recommended)
```bash
# Start all services (backend, frontend, database)
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f backend
```

Services will be available at:
- Backend API: http://localhost:5000
- Frontend: http://localhost:3000
- PostgreSQL: localhost:5432

### 3. Manual Setup

#### Backend
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your values

# Run migrations (if applicable)
flask db upgrade

# Start server
python app.py
```

#### Frontend
```bash
cd frontend
npm install
npm start
```

## Production Deployment

### Environment Variables
Create `.env` file with production values:
```bash
FLASK_ENV=production
FLASK_DEBUG=False
DATABASE_URL=postgresql://user:password@db-host:5432/dbname
JWT_SECRET_KEY=<generate-secure-256-bit-key>
CORS_ORIGINS=https://yourdomain.com
LOG_LEVEL=INFO
SENTRY_DSN=<your-sentry-dsn>
```

### Heroku/Amvera Deployment
```bash
# Login to deployment platform
heroku login  # or amvera login

# Create app
heroku create mismatch-recruiter

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set JWT_SECRET_KEY=<secure-key>
heroku config:set DATABASE_URL=<your-db-url>

# Deploy
git push heroku main
```

### Docker Deployment
```bash
# Build images
docker build -t mismatch-backend:latest ./backend
docker build -t mismatch-frontend:latest ./frontend

# Push to registry
docker tag mismatch-backend:latest registry.example.com/mismatch-backend:latest
docker push registry.example.com/mismatch-backend:latest

# Deploy with docker-compose
docker-compose -f docker-compose.prod.yml up -d
```

## Testing

### Run Tests
```bash
cd backend
pytest tests/ -v --cov=app --cov-report=html
```

### Load Testing
```bash
cd backend
pip install locust
locust -f tests/load_test.py --host=http://localhost:5000
```

## Monitoring

### Health Check
```bash
curl http://localhost:5000/health
```

### Metrics (Prometheus)
```bash
# Start Prometheus
docker run -p 9090:9090 -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus

# Access Prometheus
# http://localhost:9090
```

### Logs
```bash
# View backend logs
docker-compose logs backend

# View file logs
tail -f logs/mismatch_*.log
```

## Troubleshooting

### Database Connection Error
```bash
# Check PostgreSQL is running
docker-compose logs db

# Reset database
docker-compose down -v
docker-compose up db
```

### Port Already in Use
```bash
# Change port in docker-compose.yml or:
lsof -i :5000  # Find process
kill -9 <PID>  # Kill process
```

### Environment Variables Not Working
```bash
# Verify .env file is in correct location
ls -la backend/.env

# Check values are being read
python -c "import os; print(os.environ.get('DATABASE_URL'))"
```

## Next Steps

1. Review `PRODUCTION_CHECKLIST.md` before going live
2. Set up monitoring with Prometheus + Grafana
3. Configure alerts with Sentry
4. Set up CI/CD pipeline (GitHub Actions already configured)
5. Configure SSL/TLS certificates
6. Set up database backups
