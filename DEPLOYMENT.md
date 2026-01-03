# MisMatch Recruiter - Deployment Guide

## Overview
This document provides comprehensive instructions for deploying the MisMatch Recruiter platform using Docker and Amvera Cloud infrastructure.

## Prerequisites
- Docker 20.10+
- Docker Compose 2.0+
- Amvera CLI (for cloud deployment)
- PostgreSQL 15+
- Redis 7+

## Local Docker Deployment

### 1. Environment Configuration

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit `.env` with your specific configuration:
- Database credentials
- JWT secret key (generate with: `python -c "import secrets; print(secrets.token_urlsafe(32))")`)
- API endpoints
- Feature flags

### 2. Build Docker Image

```bash
docker build -t mismatch-recruiter:latest .
```

For multi-stage build verification:

```bash
docker build --progress=plain -t mismatch-recruiter:latest .
```

### 3. Start Services with Docker Compose

```bash
docker-compose up -d
```

This will start:
- **app**: Flask backend + React frontend (port 5000 & 3001)
- **db**: PostgreSQL database (port 5432)
- **redis**: Redis cache (port 6379)
- **nginx**: Reverse proxy (ports 80 & 443)

### 4. Initialize Database

```bash
docker-compose exec app flask db upgrade
```

### 5. Verify Deployment

Check service health:
```bash
# Check all services
docker-compose ps

# Check health endpoint
curl http://localhost:5000/health

# View logs
docker-compose logs -f app
```

## Amvera Cloud Deployment

### 1. Install Amvera CLI

```bash
curl https://amvera.ru/install.sh | sh
```

### 2. Create Amvera Application

```bash
amvera app create mismatch-recruiter
amvera cd mismatch-recruiter
```

### 3. Configure Deployment

Create `.amvera/amvera.yml`:

```yaml
app:
  name: mismatch-recruiter
  description: AI-powered recruitment platform
  version: 1.0.0

runtime:
  name: docker
  version: latest

services:
  backend:
    type: docker
    image: am.registry.cloud/mismatch-recruiter:latest
    port: 5000
    replicas: 3
    resources:
      cpu: 1000m
      memory: 512Mi
    env:
      FLASK_ENV: production
      DATABASE_URL: ${DATABASE_URL}
      REDIS_URL: ${REDIS_URL}

  frontend:
    type: static
    build: frontend
    spa: true

databases:
  postgres:
    type: postgresql
    version: 15
    storage: 10Gi

  redis:
    type: redis
    version: 7

domains:
  - name: mismatch.amvera.cloud
    ssl: true
    cors: true

scaling:
  min_replicas: 2
  max_replicas: 5
  cpu_threshold: 70
  memory_threshold: 80
```

### 4. Push and Deploy

```bash
# Login to Amvera
amvera login

# Push Docker image to Amvera registry
docker login am.registry.cloud
docker tag mismatch-recruiter:latest am.registry.cloud/mismatch-recruiter:latest
docker push am.registry.cloud/mismatch-recruiter:latest

# Deploy application
amvera deploy

# Check deployment status
amvera status
```

### 5. Database Migration

```bash
amvera app console
flask db upgrade
exit
```

## CI/CD Integration (GitHub Actions)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Amvera

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build and push image
        run: |
          docker login am.registry.cloud -u ${{ secrets.AMVERA_USER }} -p ${{ secrets.AMVERA_TOKEN }}
          docker build -t am.registry.cloud/mismatch-recruiter:${{ github.sha }} .
          docker push am.registry.cloud/mismatch-recruiter:${{ github.sha }}
      
      - name: Deploy to Amvera
        run: |
          amvera deploy --tag ${{ github.sha }}
```

## Health Checks

### Backend Health
```bash
curl -f http://localhost:5000/health || echo "Backend down"
```

### Database Health
```bash
psql -h localhost -U mismatch_user -d mismatch_db -c "SELECT 1"
```

### Redis Health
```bash
redis-cli -h localhost ping
```

## Monitoring and Logging

### View Container Logs
```bash
docker-compose logs -f app
docker-compose logs -f db
docker-compose logs -f nginx
```

### Docker Stats
```bash
docker stats
```

### Amvera Logs
```bash
amvera logs app -f
```

## Backup and Recovery

### Database Backup
```bash
docker-compose exec db pg_dump -U mismatch_user mismatch_db > backup.sql
```

### Database Restore
```bash
cat backup.sql | docker-compose exec -T db psql -U mismatch_user mismatch_db
```

## Troubleshooting

### Port Already in Use
```bash
docker-compose down
sudo lsof -i :5000
```

### Database Connection Issues
```bash
docker-compose exec db psql -U mismatch_user -d mismatch_db
```

### Clear Cache and Rebuild
```bash
docker-compose down -v
docker system prune -a
docker-compose up -d --build
```

## Security Considerations

1. **Environment Variables**: Never commit `.env` file with production secrets
2. **Docker Images**: Scan images for vulnerabilities:
   ```bash
   docker scout cves am.registry.cloud/mismatch-recruiter
   ```
3. **Network**: Use private networks for inter-service communication
4. **HTTPS**: Enable SSL/TLS for production
5. **Rate Limiting**: Configure rate limits in nginx.conf

## Performance Optimization

1. **Database Indexing**: Ensure proper database indexes
2. **Redis Caching**: Configure optimal TTL values
3. **CDN**: Use CDN for static assets
4. **Compression**: Enable gzip in nginx
5. **Scaling**: Use Amvera auto-scaling for peak loads

## Post-Deployment Checklist

- [ ] Environment variables configured
- [ ] Database migrations successful
- [ ] Health checks passing
- [ ] SSL certificates installed
- [ ] Monitoring alerts configured
- [ ] Backup strategy implemented
- [ ] Rate limiting enabled
- [ ] CORS configured correctly
- [ ] API documentation deployed
- [ ] Team notified of deployment

## Support and Resources

- Amvera Documentation: https://docs.amvera.ru
- Docker Documentation: https://docs.docker.com
- PostgreSQL Documentation: https://www.postgresql.org/docs
- Flask Documentation: https://flask.palletsprojects.com

