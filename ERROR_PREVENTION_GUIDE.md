# MisMatch Recruiter - Error Prevention & Troubleshooting Guide

**Version:** 1.0
**Date:** January 9, 2026
**Purpose:** Prevent and fix common deployment errors

## Common Issues & Solutions

### 1. Database Connection Errors

**Problem:** "psycopg2.OperationalError: could not connect to server"

**Solution:**
```bash
# Check PostgreSQL status
docker-compose ps postgres

# Check logs
docker-compose logs postgres

# Restart database
docker-compose restart postgres

# Wait 10 seconds for database to initialize
sleep 10

# Test connection
psql -h localhost -U postgres -c "SELECT 1;"
```

### 2. Redis Connection Errors

**Problem:** "ConnectionError: Error 111 connecting to localhost:6379"

**Solution:**
```bash
# Check Redis status
docker-compose ps redis

# Check Redis logs
docker-compose logs redis

# Restart Redis
docker-compose restart redis

# Test connection
redis-cli -h localhost PING
```

### 3. Port Already in Use

**Problem:** "Error starting userland proxy: listen tcp 0.0.0.0:5000: bind: address already in use"

**Solution:**
```bash
# Find process using port 5000
lsof -i :5000

# Kill process
kill -9 <PID>

# Or use docker-compose to stop all containers
docker-compose down

# Clean up
docker-compose down -v
```

### 4. Out of Memory Errors

**Problem:** "Cannot allocate memory" or "OOMKilled"

**Solution:**
```bash
# Check memory usage
docker stats

# Reduce container memory limits in docker-compose
# Or increase system memory

# Clean up images and volumes
docker system prune -a --volumes
```

### 5. Environment Variable Issues

**Problem:** "KeyError: 'DATABASE_URL'" or "ConfigError: missing required environment variable"

**Solution:**
```bash
# Check if .env file exists
ls -la .env.staging

# Verify all required variables
grep -E '^[A-Z_]+=' .env.staging | wc -l

# Source environment file
source .env.staging

# Check specific variable
echo $DATABASE_URL
```

### 6. Docker Build Failures

**Problem:** "failed to solve with frontend dockerfile.v0"

**Solution:**
```bash
# Clean up Docker cache
docker system prune -a

# Rebuild with no cache
docker-compose build --no-cache

# Check Dockerfile
cat Dockerfile | head -20
```

### 7. Dependency Import Errors

**Problem:** "ModuleNotFoundError: No module named 'xxx'"

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Check installed packages
pip list | grep -i <package-name>

# Update pip
pip install --upgrade pip
```

### 8. Staging Deployment Won't Start

**Problem:** "docker-compose up -d" shows errors

**Solution:**
```bash
# Check configuration validity
docker-compose -f docker-compose.staging.yml config

# Run with verbose output
docker-compose -f docker-compose.staging.yml up --verbose

# Check logs
docker-compose -f docker-compose.staging.yml logs -f web
```

## Validation Checklists

### Pre-Deployment
- [ ] All .env files configured
- [ ] Database initialized and accessible
- [ ] Redis cache accessible
- [ ] All dependencies installed
- [ ] Configuration syntax valid
- [ ] All ports available
- [ ] Dockerfile builds successfully
- [ ] Python syntax validated

### Post-Deployment
- [ ] All services running (docker-compose ps)
- [ ] Health endpoint responds (curl http://localhost:5000/health)
- [ ] Database connected and responsive
- [ ] Redis cache working
- [ ] Logs show no errors
- [ ] API endpoints responding
- [ ] Frontend accessible

## Email Alert Response Protocol

If you receive email alerts about errors:

1. **Check Alert Type:** Identify error category (deployment, database, performance, security)
2. **Find Solution:** Use solutions above based on error message
3. **Apply Fix:** Execute relevant commands
4. **Verify:** Run post-deployment checks
5. **Document:** Add notes to error log
6. **Monitor:** Watch logs for 10 minutes after fix

## Quick Recovery Commands

```bash
# Full restart
docker-compose down -v
docker system prune -a --volumes
Docker-compose -f docker-compose.staging.yml up -d

# Health check
docker-compose ps
curl http://localhost:5000/health
redis-cli PING
psql -c "SELECT 1;"

# Logs inspection
docker-compose logs -f web
docker-compose logs -f postgres
docker-compose logs -f redis
```

---

**Emergency Contact:** Follow escalation procedures in OPERATIONS_MANUAL.md
