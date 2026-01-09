# MisMatch Recruiter Operations Manual

**Version:** 1.0.0
**Last Updated:** January 9, 2026
**Status:** Production Ready

## System Overview

### Architecture
- **Frontend:** React + Vite (deployed on CDN)
- **Backend:** Flask + PostgreSQL + Redis
- **Workers:** Celery
- **Monitoring:** Prometheus + Grafana
- **Logging:** ELK Stack (Elasticsearch, Logstash, Kibana)
- **Containerization:** Docker + Docker Compose
- **Orchestration:** Docker Compose (development), Kubernetes (production-ready)

### Key Processes
- **User Authentication:** JWT-based authentication
- **Job Matching:** ML-powered scoring algorithm
- **Notifications:** WebSocket-based real-time updates
- **Integrations:** Lamoda OAuth2 + webhooks
- **Caching:** Redis for session and data caching
- **Database:** PostgreSQL with connection pooling

## Deployment Environments

### Local Development
- **Compose File:** docker-compose.yml
- **Frontend:** http://localhost:3000
- **Backend:** http://localhost:5000
- **Redis:** localhost:6379
- **PostgreSQL:** localhost:5432

### Staging Environment
- **Domain:** staging.mismatch-recruiter.com
- **Compose File:** docker-compose.staging.yml
- **Config:** backend/config/staging.py
- **Environment File:** .env.staging

### Production Environment
- **Domain:** mismatch-recruiter.com
- **Compose File:** docker-compose.production.yml
- **Config:** backend/config/production.py
- **Environment File:** .env.production (secured)

## Common Operational Tasks

### 1. Service Management

#### Start All Services
```bash
# Development
docker-compose up

# Staging
docker-compose -f docker-compose.staging.yml up

# Production
docker-compose -f docker-compose.production.yml up -d
```

#### Stop All Services
```bash
# Development/Staging
docker-compose down

# Production
docker-compose -f docker-compose.production.yml down
```

#### Restart Specific Service
```bash
# Restart backend
docker-compose restart web

# Restart worker
docker-compose restart celery

# Restart database
docker-compose restart postgres
```

### 2. Log Management

#### View Recent Logs
```bash
# Last 50 lines
docker-compose logs -f --tail=50 web

# Last 100 lines of worker logs
docker-compose logs -f --tail=100 celery
```

#### View Logs from Specific Time
```bash
# Last hour
docker-compose logs -f --since 1h web

# Last 30 minutes
docker-compose logs -f --since 30m web
```

#### Search Logs for Errors
```bash
# Find error messages
docker-compose logs web | grep -i error | tail -20

# Find warnings
docker-compose logs web | grep -i warning | tail -20
```

### 3. Database Management

#### Create Database Backup
```bash
# Full backup
pg_dump -h localhost -U postgres -d mismatch > backup_$(date +%Y%m%d_%H%M%S).sql

# Compressed backup
pg_dump -h localhost -U postgres -d mismatch | gzip > backup_$(date +%Y%m%d_%H%M%S).sql.gz
```

#### Restore Database from Backup
```bash
# Restore from SQL file
psql -h localhost -U postgres -d mismatch < backup_20260109_150000.sql

# Restore from compressed file
gunzip -c backup_20260109_150000.sql.gz | psql -h localhost -U postgres -d mismatch
```

#### Database Health Check
```bash
# Test connection
psql -h localhost -U postgres -d mismatch -c "SELECT 1;"

# Check connection count
psql -h localhost -U postgres -d mismatch -c "SELECT count(*) FROM pg_stat_activity;"

# List active connections
psql -h localhost -U postgres -d mismatch -c "SELECT usename, application_name, state FROM pg_stat_activity;"
```

#### Database Optimization
```bash
# VACUUM (cleanup)
psql -h localhost -U postgres -d mismatch -c "VACUUM;"

# ANALYZE (update statistics)
psql -h localhost -U postgres -d mismatch -c "ANALYZE;"

# Find slow queries (requires pg_stat_statements extension)
psql -h localhost -U postgres -d mismatch -c "SELECT query, calls, mean_time FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;"
```

### 4. Performance Monitoring

#### Docker Container Stats
```bash
# Monitor all containers
docker stats

# Monitor specific container
docker stats mismatch-web

# Monitor memory and CPU
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```

#### Redis Health
```bash
# Connect to Redis
redis-cli -h localhost

# Check Redis info
redis-cli -h localhost INFO

# Monitor commands
redis-cli -h localhost MONITOR
```

#### Prometheus Queries
```
# HTTP request rate
rate(http_requests_total[5m])

# Error rate
rate(http_requests_total{status=~"5.."}[5m])

# Cache hit ratio
rate(redis_hits_total[5m]) / (rate(redis_hits_total[5m]) + rate(redis_misses_total[5m]))

# Database query duration
histogram_quantile(0.95, rate(postgres_query_duration_seconds_bucket[5m]))
```

### 5. Troubleshooting Guide

#### Issue: High Error Rate (> 1%)

**Diagnosis:**
```bash
# Check application logs
docker-compose logs -f web | grep ERROR | head -20

# Check error rate from Prometheus
curl http://localhost:9090/api/v1/query?query='rate(http_requests_total{status=~"5.."}[5m])'
```

**Resolution:**
```bash
# 1. Check database connection
psql -h localhost -U postgres -d mismatch -c "SELECT 1;"

# 2. Restart web service
docker-compose restart web

# 3. Check Redis
redis-cli -h localhost PING

# 4. Review recent deployments
git log --oneline -10
```

#### Issue: Slow API Responses (> 500ms)

**Diagnosis:**
```bash
# Check slow queries
psql -h localhost -U postgres -d mismatch -c "
  SELECT query, calls, mean_time FROM pg_stat_statements 
  WHERE mean_time > 100 
  ORDER BY mean_time DESC LIMIT 10;
"

# Check connection pool status
psql -h localhost -U postgres -d mismatch -c "SELECT count(*) FROM pg_stat_activity;"
```

**Resolution:**
```bash
# 1. Restart database to clear connection pool
docker-compose restart postgres

# 2. Optimize slow queries
psql -h localhost -U postgres -d mismatch -c "ANALYZE;"

# 3. Check Redis cache effectiveness
redis-cli -h localhost INFO stats

# 4. Scale up worker processes if needed
docker-compose scale celery=3
```

#### Issue: Memory Leak in Backend

**Diagnosis:**
```bash
# Monitor memory growth
docker stats --format "table {{.Container}}\t{{.MemUsage}}" mismatch-web

# Check for long-running connections
psql -h localhost -U postgres -d mismatch -c "
  SELECT pid, usename, application_name, state, query_start 
  FROM pg_stat_activity 
  WHERE state != 'idle';
"
```

**Resolution:**
```bash
# Restart service
docker-compose restart web

# Or redeploy with updated code
docker-compose down
git pull
docker-compose build --no-cache
docker-compose up -d
```

#### Issue: Disk Space Running Low

**Diagnosis:**
```bash
# Check disk usage
docker exec mismatch-postgres du -sh /var/lib/postgresql/data

# Check Docker volumes
docker system df
```

**Resolution:**
```bash
# Clean up Docker images/containers
docker system prune -a --volumes

# Or backup and truncate logs
psql -h localhost -U postgres -d mismatch -c "TRUNCATE activity_logs;"
```

### 6. Scheduled Maintenance

#### Daily Tasks
- Review error logs
- Check metrics dashboard
- Verify backup completion
- Check disk space usage

#### Weekly Tasks
- Review performance trends
- Update dependencies (security patches)
- Test backup restoration
- Review slow query logs

#### Monthly Tasks
- Major dependency updates
- Database optimization (VACUUM FULL)
- Capacity planning review
- Security audit

#### Quarterly Tasks
- Performance baseline review
- Disaster recovery testing
- Infrastructure scaling review
- Incident post-mortems

### 7. Disaster Recovery

#### Database Corruption Recovery
```bash
# 1. Stop the application
docker-compose stop web celery

# 2. Stop database
docker-compose stop postgres

# 3. Restore from backup
rm -rf postgres_data
docker-compose up postgres
sleep 10
psql -h localhost -U postgres < backup_latest.sql

# 4. Verify integrity
psql -h localhost -U postgres -d mismatch -c "SELECT COUNT(*) FROM users;"

# 5. Restart services
docker-compose up -d web celery
```

#### Complete System Failure Recovery
```bash
# 1. Provision new infrastructure (manual step)

# 2. Deploy application
git clone https://github.com/maksimmishakov/mismatch-recruiter.git
cd mismatch-recruiter

# 3. Restore database
docker-compose -f docker-compose.production.yml up postgres
sleep 10
psql -h localhost -U postgres < backup_latest.sql

# 4. Deploy application services
docker-compose -f docker-compose.production.yml up -d web celery redis nginx

# 5. Verify all services
docker-compose ps
psql -h localhost -U postgres -d mismatch -c "SELECT 1;"
redis-cli -h localhost PING

# 6. Switch DNS/Load Balancer
# (Manual step in infrastructure)
```

## Emergency Contacts

- **Primary On-Call:** [Contact Information]
- **Secondary On-Call:** [Contact Information]
- **Team Manager:** [Contact Information]
- **Infrastructure Lead:** [Contact Information]

## Escalation Procedures

1. **P1 (Critical) Issues:** Page on-call immediately, escalate to manager
2. **P2 (High) Issues:** Notify on-call within 15 minutes
3. **P3 (Medium) Issues:** Address within next business day
4. **P4 (Low) Issues:** Add to backlog

## Communication Channels

- **Incidents:** #incidents (Slack)
- **Deployments:** #deployments (Slack)
- **General Ops:** #operations (Slack)
- **On-Call:** PagerDuty

---

**Last Reviewed:** January 9, 2026
**Next Review:** February 9, 2026
