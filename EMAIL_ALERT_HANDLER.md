# Email Alert Response Handler

**Automated Email Monitoring & Response Protocol**

## Alert Categories & Responses

### 1. DEPLOYMENT FAILURE ALERTS

**Alert Message Contains:** "deployment failed", "docker error", "container exited"

**Immediate Actions:**
```bash
# 1. Check services status
docker-compose ps

# 2. Review error logs
docker-compose logs -f web | head -50

# 3. Check docker events
docker events --since 1m

# 4. If needed, full restart
docker-compose down
docker-compose up -d
```

### 2. DATABASE ERRORS

**Alert Message Contains:** "database", "postgres", "connection refused"

**Immediate Actions:**
```bash
# Check postgres status
docker-compose ps postgres
docker-compose logs postgres

# Restart if needed
docker-compose restart postgres
sleep 15  # Wait for initialization

# Test connection
psql -h localhost -U postgres -c "SELECT 1;"
```

### 3. MEMORY/PERFORMANCE ALERTS

**Alert Message Contains:** "OOMKilled", "memory", "performance"

**Immediate Actions:**
```bash
# Monitor resources
docker stats --no-stream

# Clean up old images
docker image prune -a

# Clean volumes
docker volume prune -f
```

### 4. SECURITY ALERTS

**Alert Message Contains:** "security", "SSL", "certificate", "unauthorized"

**Immediate Actions:**
```bash
# Check SSL certificate
openssl s_client -connect localhost:443

# Review recent logs for suspicious activity
docker-compose logs -f web | grep -i "401\|403\|502"

# Check if authentication is working
curl -H "Authorization: Bearer <token>" http://localhost:5000/api/test
```

## Email Alert Response Template

When you receive an alert email:

1. **Note Alert Time:** Record timestamp
2. **Identify Error Type:** Match with category above
3. **Execute Commands:** Run relevant command sequence
4. **Document Fix:** Note what was done
5. **Monitor:** Watch logs for 15 minutes
6. **Notify:** Update status in monitoring system

## Automated Response Script

Create a cron job to auto-respond to common errors:

```bash
#!/bin/bash
# Check system health every 5 minutes

echo "$(date): Running health check..."

# Check if services are running
if ! docker-compose ps | grep -q "up"; then
    echo "$(date): Service down, restarting..."
    docker-compose restart
    sleep 10
fi

# Check database
if ! psql -h localhost -c "SELECT 1;" 2>/dev/null; then
    echo "$(date): Database error, restarting..."
    docker-compose restart postgres
    sleep 15
fi

# Check Redis
if ! redis-cli ping 2>/dev/null; then
    echo "$(date): Redis error, restarting..."
    docker-compose restart redis
fi

echo "$(date): Health check complete"
```

## Email Configuration

Setup email alerts in your monitoring system:

**Recipient:** <your-email@domain.com>
**Alert Threshold:** Immediate (P1), 5min (P2), 15min (P3)
**Categories:** Deployment, Database, Performance, Security
**Auto-Escalation:** After 30 minutes without resolution

