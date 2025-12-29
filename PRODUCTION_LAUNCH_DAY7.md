# ШАГ 7 — PRODUCTION LAUNCH (1-2 января, день)

## 7.1 Deployment Preparation (30 минут)

### Pre-deployment Checklist
- ✅ Code review completed
- ✅ All tests passing (9 passed)
- ✅ Security audit: OWASP Top 10
- ✅ Performance baseline established
- ✅ Database backups scheduled
- ✅ Rollback plan documented

### Architecture Overview
```
Internet → Load Balancer → Kubernetes Cluster
  ↓
  API Pods (3x replicas)
  Frontend Build (Nginx)
  ↓
  PostgreSQL (Master-Replica)
  Redis Cache
  S3 Resume Storage
```

## 7.2 Infrastructure Deployment (1 hour)

### Services Configuration
- Flask API: Port 5000
- React Frontend: Port 3000
- PostgreSQL: Port 5432
- Redis: Port 6379
- Nginx Reverse Proxy: Port 80/443

### Environment Variables (Production)
```
FLASK_ENV=production
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
JWT_SECRET=<secure-key>
AWS_S3_BUCKET=mismatch-prod
SMTP_SERVER=mail.production.com
CORS_ORIGINS=*.mismatch.com
```

### Database Migration
```bash
alembic upgrade head
psql < migrations/seed_production.sql
```

## 7.3 Monitoring & Observability (1 hour)

### Key Metrics
- API Response Time: < 200ms (p95)
- Error Rate: < 0.1%
- CPU Usage: < 70%
- Memory Usage: < 80%
- Database Connection Pool: Max 100

### Alert Thresholds
- Critical: Response Time > 500ms
- Warning: Error Rate > 1%
- Critical: Database Connections > 95

### Logging Stack
```
Application Logs → Fluentd → Elasticsearch
  ↓
  Kibana Dashboards
  ↓
  Alerting Rules → Slack/PagerDuty
```

## 7.4 Load Testing (30 минут)

### Stress Test Scenarios
- 1000 concurrent users
- Resume uploads: 500 req/sec
- Job search: 1000 req/sec
- API endpoints: 99th percentile < 300ms

### Test Tools
- Apache JMeter
- Locust
- K6 (synthetic monitoring)

## 7.5 CI/CD Pipeline (Automated)

### GitHub Actions Workflow
```yaml
name: Production Deploy
on:
  push:
    branches: [master]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - Build Docker images
      - Run security scan
      - Push to registry
      - Deploy to Kubernetes
      - Run smoke tests
      - Monitor metrics (5 min)
```

## 7.6 Post-Deployment Verification

### Health Checks
- API Health: GET /health → 200 OK
- Database: SELECT 1 → Success
- Cache: PING → PONG
- Frontend: Load time < 2s

### Smoke Tests
```bash
1. Resume Upload Flow
2. Job Search with Filters
3. Job Application Submission
4. User Profile Update
5. Payment Processing
```

## 7.7 Rollback Plan

### Immediate Rollback Trigger
- Error Rate > 5%
- Response Time p95 > 1000ms
- Database unavailable
- More than 2 services failing

### Rollback Steps
```bash
1. kubectl set image deployment/api api=old-image
2. Monitor error rates (5 min)
3. Verify database consistency
4. Notify stakeholders
5. Post-mortem within 24h
```

## Timeline
- 18:00 - Final code review + merge
- 18:30 - Database backups created
- 19:00 - Infrastructure deployment begins
- 20:00 - Load testing starts
- 20:30 - Production traffic switch (5%)
- 21:00 - Traffic increase to 25%
- 22:00 - Full traffic migration
- 22:30 - Final verification
- 23:00 - Announce production readiness

## Success Criteria
✅ All services running
✅ Error rate < 0.1%
✅ Response time p95 < 200ms
✅ 0 critical alerts
✅ 99.99% uptime first week

