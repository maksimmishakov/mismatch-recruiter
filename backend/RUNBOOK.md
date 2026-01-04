# MisMatch Recruiter - Operations Runbook

## Common Tasks

### Viewing Logs

#### Docker Logs
```bash
# Backend logs
docker-compose logs -f backend

# Frontend logs
docker-compose logs -f frontend

# Database logs
docker-compose logs -f db
```

#### File Logs
```bash
# Current day logs
tail -f logs/mismatch_$(date +%Y%m%d).log

# Last 100 lines
tail -100 logs/mismatch_*.log

# Search for errors
grep ERROR logs/mismatch_*.log
```

### Restarting Services

```bash
# Restart backend
docker-compose restart backend

# Restart frontend
docker-compose restart frontend

# Restart all services
docker-compose restart

# Force restart (kill + start)
docker-compose down && docker-compose up -d
```

## Database Management

### Backup
```bash
# Backup database
pg_dump mismatch > backup-$(date +%Y%m%d-%H%M%S).sql

# Backup with compression
pg_dump -F c mismatch > backup-$(date +%Y%m%d-%H%M%S).custom

# Backup specific table
pg_dump -t candidates mismatch > backup-candidates-$(date +%Y%m%d).sql
```

### Restore
```bash
# Restore from SQL backup
psql mismatch < backup-20260104-120000.sql

# Restore from compressed backup
pg_restore -d mismatch backup-20260104-120000.custom
```

### Queries
```bash
# Connect to database
psql -U mismatch -d mismatch

# Check active connections
psql mismatch -c "SELECT count(*) FROM pg_stat_activity;"

# Kill idle connections
psql mismatch -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE state = 'idle';"
```

## Performance Tuning

### Check Slow Queries
```bash
# PostgreSQL slow log (first 10 slow queries)
psql mismatch -c "SELECT query, mean_exec_time FROM pg_stat_statements ORDER BY mean_exec_time DESC LIMIT 10;"
```

### Clear Cache
```bash
# Redis cache
docker-compose exec cache redis-cli FLUSHALL
```

### Monitor Performance
```bash
# CPU and Memory
docker stats backend --no-stream

# Disk usage
du -sh logs/
df -h
```

## Incident Response

### High Error Rate

**Symptom**: Error rate > 5% or error count spike

**Steps**:
1. Check Sentry dashboard for error patterns
2. View backend logs: `docker-compose logs -f backend | grep ERROR`
3. Identify affected endpoint from logs
4. Check database connectivity: `psql mismatch -c "SELECT 1;"`
5. If database issue, restart: `docker-compose restart db`
6. If app issue, restart: `docker-compose restart backend`
7. Monitor metrics in Prometheus after restart

### Database Connection Issues

**Symptom**: "Connection refused" or "too many connections"

**Steps**:
1. Check PostgreSQL status: `docker-compose ps db`
2. View database logs: `docker-compose logs db`
3. Verify credentials in .env
4. Test connection: `psql -U mismatch -d mismatch -c "SELECT 1;"`
5. Check connection limit: `psql mismatch -c "SHOW max_connections;"`
6. If needed, increase limit in postgresql.conf
7. Restart database: `docker-compose restart db`

### Memory Leak

**Symptom**: Memory usage constantly increasing

**Steps**:
1. Monitor memory: `docker stats backend --no-stream`
2. Check for unclosed connections in logs
3. Review recent code changes
4. Restart service: `docker-compose restart backend`
5. Monitor memory after restart
6. If issue persists, check for database connection pool issues

### API Timeout

**Symptom**: Requests timing out (504, 408 errors)

**Steps**:
1. Check backend logs for slow queries
2. Check database load: `psql mismatch -c "SELECT count(*) FROM pg_stat_activity;"`
3. Identify slow queries: Run performance check
4. Add database indexes if needed
5. Scale backend if CPU bound: `docker-compose up -d --scale backend=3`
6. Monitor after scaling

## Monitoring Commands

### Health Check
```bash
# API health
curl http://localhost:5000/health

# Database health
psql mismatch -c "SELECT 1;"

# Redis (if used)
redis-cli ping
```

### Metrics (Prometheus)
```bash
# Query metrics
curl http://localhost:9090/api/v1/query?query=up

# Query range
curl 'http://localhost:9090/api/v1/query_range?query=up&start=1&end=2&step=15s'
```

### Alerting
```bash
# Check Sentry alerts
# Visit https://sentry.io/organizations/your-org/

# Check Prometheus alerts
# Visit http://localhost:9090/alerts
```

## Scheduled Tasks

### Daily
- [ ] Check error rates (< 1% target)
- [ ] Verify backups completed
- [ ] Monitor disk space
- [ ] Review Sentry for new patterns

### Weekly
- [ ] Review performance metrics
- [ ] Check database size growth
- [ ] Verify all services up
- [ ] Review logs for warnings

### Monthly
- [ ] Update dependencies
- [ ] Review and optimize slow queries
- [ ] Test backup restore
- [ ] Capacity planning
- [ ] Security audit

## Escalation Path

1. **On-call Engineer**: Acknowledge and assess incident (5 min)
2. **Team Lead**: Engage for major issues (15 min)
3. **Director**: Critical production issues (30 min)

## Contact Info

- **On-Call**: See Pagerduty
- **Slack**: #mismatch-alerts
- **Email**: engineering@mismatch.io
