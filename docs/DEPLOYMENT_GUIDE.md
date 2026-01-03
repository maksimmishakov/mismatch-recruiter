# 🚀 MisMatch Recruiter - Production Deployment Guide

## System Requirements
- Docker & Docker Compose
- Node.js 18+ (for local development)
- Python 3.10+ (for local development)
- 4GB RAM minimum
- 20GB disk space minimum

## Deployment Architecture

### Multi-Stage Docker Build
```
Builder Stage: Node.js 18-Alpine → Build frontend
Runtime Stage: Node.js 18-Alpine → Serve frontend on port 3000
```

### Services
- Frontend: React application (Port 3000)
- Backend: Flask API (Port 5000)
- Database: PostgreSQL (Port 5432)
- Cache: Redis (Port 6379)

## Quick Start

### 1. Build Docker Image
```bash
docker build -t mismatch-recruiter:v1.0.0 .
```

### 2. Deploy with Docker Compose
```bash
docker-compose up -d
```

### 3. Run Migrations
```bash
docker-compose exec web python -m alembic upgrade head
```

### 4. Verify Deployment
```bash
curl http://localhost:3000
curl http://localhost:5000/health
```

## Production Deployment (Amvera)

### 1. Prepare Environment
```bash
# Set production environment variables
export AMVERA_ACCOUNT_ID=your_account_id
export AMVERA_TOKEN=your_auth_token
export APP_ENV=production
export DEBUG=false
```

### 2. Deploy to Amvera
```bash
# Using blue-green deployment for zero downtime
bash deployment/blue_green_deploy.sh
```

### 3. Verify Production Health
```bash
curl https://mismatch-recruiter.amvera.io/health
```

## Monitoring

### Application Logs
```bash
docker-compose logs -f web
```

### Performance Metrics
```bash
docker stats
```

### Database Health
```bash
docker-compose exec db psql -U postgres -d mismatch_recruiter -c "SELECT * FROM pg_stat_statements LIMIT 10;"
```

