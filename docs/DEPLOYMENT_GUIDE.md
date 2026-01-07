# Deployment Guide

## Environments

### Development
```bash
docker-compose up --build
```

### Production
```bash
# Build and push images
docker build -t mismatch-recruiter:latest backend/
# Deploy on Amvera Cloud
```

## Pre-deployment Checklist
- All tests passing
- Coverage > 80%
- No security vulnerabilities
- Environment variables configured
- Database migrations applied

## Monitoring & Logs
- Container logs: `docker logs <container_id>`
- Application logs: `/app/logs/`
- Health check: `GET /health`
