# Operational Runbook
## mismatch-recruiter Production Operations

## Daily Operations

### Morning Checklist (9 AM)
- [ ] Verify all services are healthy
- [ ] Check error logs from overnight
- [ ] Monitor database size
- [ ] Verify backups completed
- [ ] Review performance metrics

### Continuous Monitoring
- Dashboard: http://localhost:3001 (Grafana)
- Logs: Docker logs or ELK stack
- Alerts: Configured in Prometheus

## Common Tasks

### Scaling
```bash
# Horizontal scaling
docker-compose up -d --scale backend=3

# Resource limits
docker-compose up -d --cpus=2 --memory=4g
```

### Database Maintenance
```bash
# Backup
docker exec postgres pg_dump -U postgres > backup.sql

# Restore
docker exec -i postgres psql -U postgres < backup.sql

# Optimize
docker exec postgres vacuumdb -U postgres
```

### Log Management
```bash
# View logs
docker-compose logs -f backend

# Clear logs
docker system prune --volumes

# Archive logs
tar -czf logs-$(date +%Y%m%d).tar.gz /var/log/mismatch/
```

## Troubleshooting

### Service Down
1. Check health: `curl http://localhost:5000/health`
2. Review logs: `docker-compose logs backend`
3. Restart: `docker-compose restart backend`
4. If persistent, redeploy from backup

### Performance Issues
1. Check CPU/Memory: `docker stats`
2. Review slow queries in logs
3. Scale horizontally if needed
4. Check database indexes

### Database Issues
1. Check connections: `docker exec postgres psql -U postgres -c "SELECT count(*) FROM pg_stat_activity"`
2. Kill long-running: `docker exec postgres pg_terminate_backend(pid)`
3. Restore from backup if corrupted

## Escalation
- Level 1: Ops Team (30 min response)
- Level 2: DevOps Lead (1 hour response)
- Level 3: CTO (4 hour response)
