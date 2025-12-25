# Amvera Cloud Deployment Guide

## Prerequisites
- Amvera Cloud account
- Docker installed locally
- Amvera CLI installed
- Git configured

## Step-by-Step Deployment

### 1. Create Amvera Project
```bash
amvera project create lamoda-recruiter --region eu-central-1
amvera project select lamoda-recruiter
```

### 2. Configure Database
```bash
# Create PostgreSQL database on Amvera
amvera db create postgres \
  --name lamoda_recruiter \
  --version 15 \
  --size small \
  --backup enabled

# Wait for database to be ready
amvera db wait postgres

# Get database credentials
amvera db credentials postgres > db-credentials.txt
```

### 3. Configure Redis Cache
```bash
# Create Redis cache
amvera cache create redis \
  --version 7 \
  --size small \
  --persistence enabled

# Get Redis URL
amvera cache credentials redis
```

### 4. Set Environment Secrets
```bash
# Set all required secrets
amvera secret set DATABASE_URL "postgresql://user:pass@db.amvera:5432/lamoda_recruiter"
amvera secret set REDIS_URL "redis://cache.amvera:6379/0"
amvera secret set JWT_SECRET_KEY "your-secret-key"
amvera secret set STRIPE_API_KEY "sk_live_xxxxx"
amvera secret set AMVERA_API_KEY "your-amvera-api-key"

# Verify secrets
amvera secret list
```

### 5. Deploy Application
```bash
# Option A: Using script (recommended)
./scripts/deploy-amvera.sh

# Option B: Manual deployment
# Build Docker image
docker build -t ghcr.io/maksimmishakov/lamoda-recruiter:latest .

# Push to registry
docker push ghcr.io/maksimmishakov/lamoda-recruiter:latest

# Deploy
amvera deploy -f .amvera/deployment.yaml
```

### 6. Verify Deployment
```bash
# Check pod status
amvera get pods -n production

# Check services
amvera get services -n production

# Get application URL
amvera service info lamoda-recruiter-service

# Test health endpoint
curl http://YOUR_APP_URL/api/health
```

### 7. Configure Monitoring
```bash
# Setup monitoring
amvera monitoring enable
amvera monitoring create-dashboard \
  --name "MisMatch Recruiter" \
  --metrics cpu,memory,requests,errors

# Create alerts
amvera alert create \
  --name "High CPU Usage" \
  --metric cpu \
  --threshold 80 \
  --action notify
```

## Scaling Configuration

### Auto-scaling Rules
```yaml
# Already configured in .amvera/deployment.yaml
minReplicas: 3
maxReplicas: 10
cpuThreshold: 70%
memoryThreshold: 80%
```

### Manual Scaling
```bash
# Scale to N replicas
amvera scale deployment/lamoda-recruiter --replicas 5
```

## Monitoring & Logging

### View Logs
```bash
# Real-time logs
amvera logs -f deployment/lamoda-recruiter

# Historical logs
amvera logs --since 1h deployment/lamoda-recruiter
```

### Metrics
```bash
# View CPU usage
amvera metrics cpu deployment/lamoda-recruiter

# View memory usage
amvera metrics memory deployment/lamoda-recruiter

# View request count
amvera metrics requests deployment/lamoda-recruiter
```

## Troubleshooting

### Pod not starting
```bash
# Check pod events
amvera describe pod lamoda-recruiter-xxxxx

# Check logs
amvera logs deployment/lamoda-recruiter
```

### Database connection issues
```bash
# Verify database is running
amvera db status postgres

# Test connection
amvera db test postgres

# Check connection string
amvera secret get DATABASE_URL
```

### Out of memory
```bash
# Check memory usage
amvera metrics memory deployment/lamoda-recruiter

# Increase memory limit
amvera set deployment/lamoda-recruiter memory 1Gi
```
