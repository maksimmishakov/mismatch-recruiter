# Deployment Guide - MisMatch Recruiter

## Table of Contents
1. [Local Development](#local-development)
2. [Staging Deployment](#staging-deployment)
3. [Production Deployment](#production-deployment)
4. [Monitoring & Alerts](#monitoring--alerts)
5. [Troubleshooting](#troubleshooting)

## Local Development

### Prerequisites
- Docker & Docker Compose
- Git
- Python 3.12 (for local backend development)
- Node 20 (for local frontend development)

### Setup

```bash
# Clone repository
git clone https://github.com/yourorg/mismatch-recruiter.git
cd mismatch-recruiter

# Start all services
docker-compose up -d

# Wait for services to be healthy
sleep 10

# Verify deployment
docker-compose ps

# Check health
curl http://localhost:5000/health
```

### Services
- **Backend**: http://localhost:5000
- **Frontend**: http://localhost:3000
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000

## Staging Deployment

### Using Amvera Cloud

1. **Configure Amvera CLI**
```bash
amvera login
amvera set-domain mismatch-staging
```

2. **Deploy to Staging**
```bash
# Push to Amvera
git push amvera develop

# Check deployment status
amvera app info mismatch-staging
```

3. **Run Tests in Staging**
```bash
# SSH into staging
amvera ssh mismatch-staging

# Run tests
cd /app/backend
pytest tests/ -v
```

## Production Deployment

### Pre-Deployment Checklist

- [ ] All tests passing locally
- [ ] All GitHub Actions workflows green
- [ ] Code review completed
- [ ] Security scan passed
- [ ] Database backup created
- [ ] Monitoring configured
- [ ] Rollback plan prepared

### Deployment Steps

1. **Create Release Tag**
```bash
git tag -a v1.0.0 -m "Production Release v1.0.0"
git push origin v1.0.0
```

2. **Deploy to Production**
```bash
# Push to production branch
git push origin main

# This automatically triggers GitHub Actions deployment workflow
# Monitor progress at: https://github.com/yourorg/mismatch-recruiter/actions
```

3. **Verify Deployment**
```bash
# Check health
curl https://api.mismatch-recruiter.amvera.io/health

# Check logs
amvera applogs mismatch-recruiter -f

# Verify frontend
curl https://mismatch-recruiter.amvera.io
```

4. **Run Smoke Tests**
```bash
# Health check
curl -I https://api.mismatch-recruiter.amvera.io/health

# API test
curl https://api.mismatch-recruiter.amvera.io/api/candidates

# Database connectivity
# Check through monitoring dashboards
```

### Environment Variables (Production)

Set these in Amvera dashboard or CI/CD secrets:

```bash
FLASK_ENV=production
FLASK_DEBUG=False
DATABASE_URL=postgresql://[user]:[password]@[host]:[port]/[db]
JWT_SECRET_KEY=[generate-256-bit-key]
CORS_ORIGINS=https://mismatch-recruiter.amvera.io,https://www.mismatch-recruiter.amvera.io
LOG_LEVEL=INFO
SENTRY_DSN=[your-sentry-dsn]
AMVERA_TOKEN=[ci-cd-token]
```

## Monitoring & Alerts

### Prometheus Metrics

Access at: `https://prometheus.mismatch-recruiter.amvera.io`

**Key Metrics to Monitor:**
- `mismatch_requests_total` - Total HTTP requests
- `mismatch_request_duration_seconds` - Request latency
- `mismatch_errors_total` - Error count
- `mismatch_active_candidates` - Active candidates count
- `mismatch_db_queries_total` - Database queries

### Grafana Dashboards

Access at: `https://grafana.mismatch-recruiter.amvera.io`

**Dashboards:**
1. System Health (CPU, Memory, Disk)
2. API Performance (Response times, Error rates)
3. Database (Connection count, Query performance)
4. Business Metrics (Active candidates, Matches created)

### Sentry Error Tracking

Access at: `https://sentry.io/organizations/yourorg/projects/mismatch/`

**Alert Rules:**
- Error rate > 1% → Slack notification
- New error type → Email notification
- Performance degradation → PagerDuty alert

### Alerting Rules

Configured in `alerting-rules.yml`:

```yaml
Groups:
  - name: mismatch-production
    interval: 30s
    rules:
      - alert: HighErrorRate
        expr: rate(mismatch_errors_total[5m]) > 0.05
        for: 5m
        annotations:
          summary: "High error rate detected"
          
      - alert: HighResponseTime
        expr: histogram_quantile(0.95, mismatch_request_duration_seconds) > 1
        for: 5m
        annotations:
          summary: "High response time detected"
```

## Troubleshooting

### Backend Not Starting

```bash
# Check logs
amvera applogs mismatch-recruiter -f

# Common issues:
# 1. Environment variables not set
echo $DATABASE_URL  # Should not be empty

# 2. Database not accessible
psql $DATABASE_URL -c "SELECT 1"

# 3. Port already in use
lsof -i :5000
```

### Database Issues

```bash
# Connect to database
psql postgresql://[user]:[password]@[host]:[port]/[db]

# Check tables
\dt

# Check connections
SELECT datname, count(*) FROM pg_stat_activity GROUP BY datname;

# Restore from backup
psql [database] < backup-2026-01-08.sql
```

### Memory Issues

```bash
# Check memory usage
free -h

# Clear Redis cache
amvera ssh mismatch-recruiter
redis-cli FLUSHALL

# Restart service
amvera app restart mismatch-recruiter
```

### Performance Issues

```bash
# Slow query log analysis
SELECT query, mean_time, max_time 
FROM pg_stat_statements 
ORDER BY mean_time DESC LIMIT 10;

# Check active connections
SELECT usename, query FROM pg_stat_activity;

# Analyze query plan
EXPLAIN ANALYZE SELECT * FROM candidates WHERE status = 'active';
```

### Rollback Procedure

If deployment fails:

```bash
# Check recent deployments
git log --oneline -10

# Rollback to previous version
git revert HEAD
git push origin main

# Or checkout specific tag
git checkout v0.9.0
git push origin main --force

# Verify rollback
curl https://api.mismatch-recruiter.amvera.io/health
```

## Security Considerations

1. **Environment Variables**: Never commit secrets
   ```bash
   # Use .env.production.local (never commit)
   cat .env.production.local >> .gitignore
   ```

2. **Database Backups**: Automated daily backups
   ```bash
   # Backup script in cron
   0 2 * * * /scripts/backup-db.sh
   ```

3. **SSL/TLS**: Auto-enabled by Amvera
   - HTTPS only
   - Certificate auto-renewal

4. **Rate Limiting**: Configured per endpoint
   - Auth: 5 requests/hour
   - API: 50 requests/hour
   - Public: 200 requests/day

## Support & Escalation

**On-Call Team**: ops-mismatch@example.com  
**Slack Channel**: #mismatch-production  
**PagerDuty**: [Link to on-call schedule]  
**Runbook**: See RUNBOOK.md

