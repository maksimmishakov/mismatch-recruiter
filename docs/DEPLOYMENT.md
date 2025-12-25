# Deployment Guide

## Overview
Comprehensive guide for deploying the MisMatch Recruitment Bot to production environments.

## Prerequisites

- Docker and Docker Compose
- Kubernetes cluster (for production)
- Terraform (for infrastructure as code)
- PostgreSQL 14+
- Redis 6+
- Python 3.11+
- GitHub Actions enabled
- Yandex Cloud account or Amvera account

## Development Environment Setup

### 1. Local Development

```bash
# Clone the repository
git clone https://github.com/maksimmishakov/lamoda-ai-recruiter.git
cd lamoda-ai-recruiter

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup PostgreSQL locally
sudo docker run -d --name postgres -p 5432:5432 \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=lamoda \
  postgres:14

# Setup Redis locally
sudo docker run -d --name redis -p 6379:6379 redis:6

# Create environment file
cp .env.example .env
# Edit .env with your local settings

# Run migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --port 8000
```

### 2. Environment Variables

```bash
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/lamoda
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20

# Redis Configuration
REDIS_URL=redis://localhost:6379/0
REDIS_PASSWORD=
REDIS_SSL=false

# OpenAI Configuration
OPENAI_API_KEY=sk-xxx
OPENAI_MODEL=gpt-4o-mini
OPENAI_TIMEOUT=30

# JWT Configuration
JWT_SECRET=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# API Configuration
API_TITLE=MisMatch Recruitment Bot
API_VERSION=1.0.0
API_WORKERS=4
API_TIMEOUT=30
LOG_LEVEL=INFO

# Rate Limiting
RATE_LIMIT_REQUESTS=1000
RATE_LIMIT_PERIOD=3600

# CORS Settings
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
```

## Docker Deployment

### 1. Build Docker Image

```bash
# Build image
docker build -t lamoda-recruiter:latest .

# Tag for registry
docker tag lamoda-recruiter:latest registry.yandex.cloud/lamoda/recruiter:latest
```

### 2. Docker Compose for Local Development

```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/lamoda
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    volumes:
      - ./app:/app/app

  db:
    image: postgres:14
    environment:
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=lamoda
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:6
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

Run with: `docker-compose up`

## Yandex Cloud Deployment

### 1. Prerequisites

- Yandex Cloud CLI installed and configured
- Cloud functions or VM instance
- Container Registry set up

### 2. Deploy to Cloud Run / Cloud Functions

```bash
# Set environment
export YANDEX_CLOUD_ID="your-cloud-id"
export YANDEX_FOLDER_ID="your-folder-id"

# Push image to registry
docker push registry.yandex.cloud/lamoda/recruiter:latest

# Deploy using Terraform
cd terraform
terraform init
terraform plan
terraform apply
```

### 3. Terraform Configuration

```hcl
resource "yandex_serverless_container" "recruiter" {
  name               = "lamoda-recruiter"
  memory             = 512
  cpu                = 100
  execution_timeout  = "30s"

  image {
    url = "registry.yandex.cloud/lamoda/recruiter:latest"
  }

  environment = {
    DATABASE_URL = var.database_url
    REDIS_URL    = var.redis_url
    OPENAI_API_KEY = var.openai_api_key
  }
}
```

## Amvera Deployment

### 1. Connect GitHub Repository

1. Log in to Amvera (https://cloud.amvera.ru)
2. Create new application
3. Connect GitHub repository
4. Select `master` branch for continuous deployment

### 2. Configure Environment Variables

In Amvera console:
```
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
OPENAI_API_KEY=sk-...
```

### 3. Amvera Configuration (amvera.yml)

```yaml
name: lamoda-recruiter
type: python
runtime: python311

buildpack:
  requirements: requirements.txt

instances:
  count: 1
  memory: 512M

scaling:
  auto_scale:
    enabled: true
    min_instances: 1
    max_instances: 3

health_check:
  path: /health
  port: 8000
  timeout: 5
  interval: 10
```

### 4. Deploy

```bash
# Push to master triggers automatic deployment
git push origin master

# Or manually deploy
amvera deploy
```

## Kubernetes Deployment

### 1. Create Kubernetes Manifests

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: lamoda-recruiter
spec:
  replicas: 3
  selector:
    matchLabels:
      app: lamoda-recruiter
  template:
    metadata:
      labels:
        app: lamoda-recruiter
    spec:
      containers:
      - name: recruiter
        image: registry.yandex.cloud/lamoda/recruiter:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: database-url
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: redis-url
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: openai-api-key
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: lamoda-recruiter
spec:
  selector:
    app: lamoda-recruiter
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

### 2. Deploy to Kubernetes

```bash
kubectl create namespace lamoda
kubectl create secret generic app-secrets \
  --from-literal=database-url=$DATABASE_URL \
  --from-literal=redis-url=$REDIS_URL \
  --from-literal=openai-api-key=$OPENAI_API_KEY \
  -n lamoda

kubectl apply -f deployment.yaml -n lamoda
kubectl apply -f service.yaml -n lamoda
```

## CI/CD Pipeline (GitHub Actions)

### 1. Automated Testing

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest --cov=app tests/
```

### 2. Automated Deployment

```yaml
name: Deploy
on:
  push:
    branches: [master]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build and push Docker image
        run: |
          docker build -t registry.yandex.cloud/lamoda/recruiter:${{ github.sha }} .
          docker push registry.yandex.cloud/lamoda/recruiter:${{ github.sha }}
      - name: Deploy to Amvera
        run: amvera deploy
```

## Database Migrations

### 1. Alembic Setup

```bash
# Create migration
alembic revision --autogenerate -m "Add users table"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

### 2. Production Migrations

```bash
# Create backup before migration
pg_dump $DATABASE_URL > backup.sql

# Apply migrations
alembic upgrade head

# Verify
alembic current
```

## Monitoring and Logging

### 1. Application Logs

```bash
# Check logs in Amvera
amvera logs

# Local logs
journalctl -u lamoda-recruiter -f
```

### 2. Performance Monitoring

```python
# Add monitoring endpoints
@app.get("/metrics")
async def metrics():
    return {
        "requests_total": prometheus_client.REGISTRY.metrics(),
        "database_pool": db_pool.size(),
    }
```

## Troubleshooting

### Common Issues

1. **Connection timeout to database**
   - Check DATABASE_URL environment variable
   - Verify database is running
   - Check firewall rules

2. **Redis connection failed**
   - Verify REDIS_URL is correct
   - Check Redis service status
   - Verify credentials

3. **OpenAI API errors**
   - Verify API key is valid
   - Check API quotas
   - Review rate limits

## Rollback Procedure

```bash
# Rollback to previous version
amvera deploy --revision previous

# Or manually
git revert <commit-hash>
git push origin master
```

## Security Checklist

- [ ] Change JWT secret in production
- [ ] Use HTTPS only
- [ ] Enable database backups
- [ ] Configure firewall rules
- [ ] Rotate API keys regularly
- [ ] Enable application logging
- [ ] Use secrets manager for sensitive data
- [ ] Configure CORS properly

## Performance Optimization

### 1. Database Optimization

```sql
CREATE INDEX idx_candidates_email ON candidates(email);
CREATE INDEX idx_interviews_candidate_id ON interviews(candidate_id);
CREATE INDEX idx_responses_interview_id ON responses(interview_id);
```

### 2. Caching Strategy

- Cache interview questions for 24 hours
- Cache evaluation results for 30 days
- Implement cache invalidation on updates

### 3. Connection Pooling

```python
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True
)
```

## Support and Documentation

For issues and questions:
- GitHub Issues: https://github.com/maksimmishakov/lamoda-ai-recruiter/issues
- Email: support@lamoda.ru
- Documentation: https://docs.lamoda.ru
