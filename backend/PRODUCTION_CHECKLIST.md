# Production Deployment Checklist

## Pre-Deployment (1 week before)

### Environment & Configuration
- [ ] All environment variables set in production
- [ ] JWT_SECRET_KEY is 256-bit and secure
- [ ] CORS_ORIGINS configured for production domains
- [ ] LOG_LEVEL set to INFO
- [ ] SENTRY_DSN configured for error tracking
- [ ] Database URL points to production PostgreSQL
- [ ] Database backed up before deployment
- [ ] SSL/TLS certificates obtained and installed

### Security Review
- [ ] All secrets removed from code
- [ ] .env file is in .gitignore
- [ ] No hardcoded API keys or passwords
- [ ] HTTPS/TLS enabled
- [ ] Security headers configured (CSP, HSTS)
- [ ] Rate limiting enabled (200/day, 50/hour)
- [ ] Input validation enabled
- [ ] SQL injection protection verified
- [ ] XSS protection enabled
- [ ] CSRF protection configured

### Code Quality
- [ ] All tests passing (pytest)
- [ ] Code coverage > 80%
- [ ] No console.log in production code
- [ ] Linting passed (eslint, pylint)
- [ ] Type checking passed (TypeScript)
- [ ] No TODO/FIXME comments for production
- [ ] Database migrations up to date

### Infrastructure
- [ ] PostgreSQL running and accessible
- [ ] Database backups configured (daily)
- [ ] Prometheus metrics working
- [ ] Sentry project created and configured
- [ ] ELK stack or log aggregation ready
- [ ] Firewall rules configured
- [ ] CDN configured (if applicable)
- [ ] Load balancer configured

### Monitoring & Alerting
- [ ] Health checks configured
- [ ] Alerting rules deployed
- [ ] Grafana dashboards created
- [ ] On-call rotation established
- [ ] Runbook prepared
- [ ] Incident response plan ready
- [ ] Escalation policy defined

## Deployment Day

### Pre-Deployment Commands
```bash
# 1. Run full test suite
cd backend && pytest tests/ -v --cov=app
cd frontend && npm run build && npm run test

# 2. Security scan
cd backend && bandit -r app/

# 3. Database backup
pg_dump mismatch > backup-$(date +%Y%m%d-%H%M%S).sql

# 4. Build Docker images
docker build -t mismatch-backend:1.0.0 ./backend
docker build -t mismatch-frontend:1.0.0 ./frontend

# 5. Run smoke tests
curl http://localhost:5000/health
```

### Deployment Steps
- [ ] Deploy backend service
- [ ] Deploy frontend service
- [ ] Run database migrations
- [ ] Verify health checks passing
- [ ] Run smoke tests
- [ ] Monitor error rates in Sentry

### Post-Deployment
- [ ] Verify all endpoints responding
- [ ] Check database connectivity
- [ ] Verify metrics in Prometheus
- [ ] Check logs for errors
- [ ] Test authentication flow
- [ ] Test core workflows
- [ ] Monitor performance metrics
- [ ] Verify automated backups running

## Rollback Plan

If deployment fails:
```bash
# 1. Revert to previous version
git revert HEAD
gh workflow run deploy.yml --ref main

# 2. Or manually rollback
docker pull registry.example.com/mismatch-backend:1.0.0-prev
docker-compose down && docker-compose up

# 3. Verify services recovering
docker-compose ps
curl http://localhost:5000/health

# 4. Check monitoring dashboards
# Open Prometheus, Grafana, Sentry

# 5. Notify team
# Send notification to incident channel
```

## Post-Deployment Monitoring (First Week)

### Daily Checks
- [ ] Error rate < 1%
- [ ] Response time p95 < 500ms
- [ ] Database query p95 < 100ms
- [ ] No memory leaks detected
- [ ] No CPU spikes
- [ ] Disk space sufficient (> 20% free)
- [ ] Backups running successfully
- [ ] Logs being collected

### Weekly Review
- [ ] Performance metrics baseline established
- [ ] Security logs reviewed
- [ ] Error patterns analyzed
- [ ] User feedback collected
- [ ] Capacity planning done
- [ ] Incident review completed

## Sign-Off

- [ ] Tech Lead: __________________ Date: __________
- [ ] DevOps: __________________ Date: __________
- [ ] Product: __________________ Date: __________

## Version Information

- Backend Version: __________
- Frontend Version: __________
- Database Version: PostgreSQL 15+
- Deployment Date: __________
- Deployment Duration: __________
