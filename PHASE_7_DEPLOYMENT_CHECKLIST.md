# Phase 7 Deployment Pipeline Checklist

## Overview
This checklist ensures all Phase 7 components are properly configured and tested before deploying to staging and production.

## Pre-Deployment (24 hours before)

### Infrastructure
- [ ] Staging server access verified
- [ ] Production server access verified
- [ ] DNS records verified (staging and production)
- [ ] SSL certificates obtained and installed
- [ ] Database backups automated
- [ ] Backup storage verified (separate from production)

### Configuration Files Created
- [x] `backend/config/staging.py` - Staging configuration
- [x] `backend/config/production.py` - Production configuration
- [x] `docker-compose.staging.yml` - Staging Docker Compose
- [x] `.env.staging.template` - Environment template
- [x] `.github/workflows/deploy-staging.yml` - GitHub Actions staging workflow
- [x] `nginx/mismatch-staging.conf` - Nginx staging config
- [x] `scripts/setup-ssl.sh` - SSL setup script
- [x] `scripts/verify-deployment.sh` - Verification script
- [x] `backend/monitoring/prometheus.yml` - Prometheus config

## Staging Deployment

### Pre-Deployment
- [ ] Backup staging database
- [ ] Take screenshot of current metrics
- [ ] Verify all services healthy
- [ ] SSH key working
- [ ] Deployment script tested locally

### Deployment Steps
1. [ ] Push code to develop branch
   ```bash
   git checkout develop
   git pull origin develop
   git add -A
   git commit -m "Phase 7: Deployment pipeline setup"
   git push origin develop
   ```

2. [ ] GitHub Actions workflow triggered
   - Monitor: https://github.com/maksimmishakov/mismatch-recruiter/actions
   - Wait for Docker image build
   - Wait for deploy-staging job

3. [ ] Services started successfully
   - [ ] API health check: `curl https://staging-api.mismatch-recruiter.ru/api/health`
   - [ ] Frontend loads: `https://staging.mismatch-recruiter.ru`
   - [ ] Grafana dashboard: `https://staging.mismatch-recruiter.ru:3001`

4. [ ] Run verification tests
   ```bash
   ./scripts/verify-deployment.sh staging
   ```

### Post-Deployment Testing
- [ ] All API endpoints responding
- [ ] Database migrations applied
- [ ] Redis cache working
- [ ] Celery tasks processing
- [ ] Email notifications sending
- [ ] Monitoring dashboards populated
- [ ] Error tracking (Sentry) working
- [ ] No unexpected errors in logs

## Production Deployment (Blue-Green)

### 1 Hour Before
- [ ] Final code review completed
- [ ] All staging tests passed
- [ ] Team notified (Slack, email)
- [ ] On-call engineer assigned
- [ ] Incident channel open
- [ ] Rollback plan reviewed

### Canary Deployment (10% Traffic)
1. [ ] Trigger canary deployment
2. [ ] Monitor error rate (should be < 1%)
3. [ ] Monitor response time (should be < 200ms)
4. [ ] Check database performance
5. [ ] Check memory/CPU usage
6. [ ] Wait 10 minutes
7. [ ] Metrics looking good? Proceed to full deployment

### Full Production Deployment
1. [ ] Blue-Green deployment initiated
2. [ ] New deployment (green) started
3. [ ] Health checks passing
4. [ ] Smoke tests passed
5. [ ] Traffic switched to green (100%)
6. [ ] Blue deployment kept as fallback

### Post-Deployment Verification
- [ ] API responding correctly
- [ ] User requests processing
- [ ] Database queries healthy
- [ ] Error rate stable (< 0.1%)
- [ ] Response time normal (< 200ms)
- [ ] Celery tasks processing
- [ ] Redis cache hit rate (> 80%)
- [ ] CPU usage normal (< 70%)
- [ ] Memory usage normal (< 80%)
- [ ] Disk space available

### Production Testing (30 minutes)
- [ ] All endpoints tested
- [ ] Authentication working
- [ ] Data integrity verified
- [ ] Edge cases tested
- [ ] Production logs reviewed

### Stakeholder Notification
- [ ] Team notified success
- [ ] Metrics dashboard shared
- [ ] Deployment recorded
- [ ] Blog post/announcement prepared
- [ ] Internal communication sent

## Post-Deployment (24 hours)

### Monitoring
- [ ] Metrics trends normal
- [ ] Error rate stable
- [ ] User metrics (DAU, MAU) tracking
- [ ] Performance metrics stable
- [ ] Database health good
- [ ] No unexpected errors

### Cleanup
- [ ] Docker images cleaned up
- [ ] Old logs archived
- [ ] Database cleanup run
- [ ] Temporary files deleted

### Lessons Learned
- [ ] Deployment time recorded
- [ ] Any issues documented
- [ ] Improvements identified
- [ ] Runbook updated
- [ ] Team feedback gathered

## Rollback Procedure (If Needed)

### Decision Criteria
- Error rate > 5%
- Response time > 5s
- Database corruption risk
- User-impacting outage

### Rollback Steps
1. [ ] Team consensus required (3 leads)
2. [ ] Trigger rollback workflow
   ```bash
   gh workflow run rollback-production.yml -f version=v1.0.0
   ```
3. [ ] Traffic switched back to blue
4. [ ] Verify services restored
5. [ ] Run smoke tests
6. [ ] Monitor error rate
7. [ ] Document root cause
8. [ ] Schedule post-mortem

## Completion

Phase 7 is complete when:
- ✅ All configuration files created and tested
- ✅ GitHub Actions workflows deployed
- ✅ Staging deployment successful
- ✅ Production deployment successful
- ✅ All monitoring working
- ✅ Team trained on deployment process

**Timeline**: 2-3 days
