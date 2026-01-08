# 🚀 PHASE 6 DEPLOYMENT & OPERATIONS GUIDE

**Last Updated**: January 8, 2026  
**Status**: Production-Ready  
**Version**: 1.0  

---

## 📚 Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Environment Setup](#environment-setup)
3. [Docker Deployment](#docker-deployment)
4. [Performance Validation](#performance-validation)
5. [Monitoring Setup](#monitoring-setup)
6. [Operations & Maintenance](#operations--maintenance)
7. [Troubleshooting](#troubleshooting)

---

## ✅ Pre-Deployment Checklist

### Infrastructure Requirements
- [ ] Linux/Unix server with Docker and Docker Compose
- [ ] Minimum 2GB RAM
- [ ] Minimum 20GB disk space
- [ ] Network access for external API calls

### Software Requirements
- [ ] Python 3.9+
- [ ] PostgreSQL 13+
- [ ] Redis 6+
- [ ] Docker 20.10+
- [ ] Docker Compose 2.0+

### Configuration Files
- [ ] `.env` file with all required variables
- [ ] `requirements.txt` updated
- [ ] Database migrations prepared
- [ ] SSL certificates (for HTTPS)

---

## 🎛️ Environment Setup

### 1. Clone Repository
```bash
git clone https://github.com/maksimmishakov/mismatch-recruiter.git
cd mismatch-recruiter
```

### 2. Create Environment File
```bash
cat > .env << 'ENVEOF'
FLASK_ENV=production
DATABASE_URL=postgresql://username:password@postgres:5432/mismatch
JWT_SECRET_KEY=your-secret-key-here-minimum-32-characters
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/1
REDIS_HOST=redis
REDIS_PORT=6379
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=40
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=1800
ENVEOF
```

### 3. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
cd ..
```

---

## 🚢 Docker Deployment

### Development
```bash
docker-compose up --build
```

### Production
```bash
# Build images
docker-compose -f docker-compose.yml build

# Start services
docker-compose -f docker-compose.yml up -d

# Verify services
docker-compose ps

# Check logs
docker-compose logs -f backend
```

### Service Health
```bash
# Check API
curl http://localhost:5000/api/health

# Check Prometheus
curl http://localhost:9090/-/healthy

# Check Redis
redis-cli ping
```

---

## 📊 Performance Validation

### 1. Run Load Tests
```bash
# Small test (10 concurrent users)
k6 run backend/scripts/loadtest_candidates.js

# Large test (500 concurrent users)
k6 run -u 500 -d 5m backend/scripts/loadtest_candidates.js

# Export results
k6 run -o json=results.json backend/scripts/loadtest_candidates.js
```

### 2. Analyze Results
```bash
python3 backend/scripts/analyze_performance.py results.json
```

### 3. Performance Targets
| Metric | Target | Current |
|--------|--------|----------|
| p95 Response Time | <45ms | TBD |
| Throughput | >1000 req/s | TBD |
| Error Rate | <0.1% | TBD |
| Memory Usage | <500MB | TBD |

---

## 📋 Monitoring Setup

### Prometheus
**URL**: http://localhost:9090

**Key Metrics**:
- `flask_http_request_duration_seconds` - API response time
- `flask_http_requests_total` - Total requests
- `database_connection_pool_checked_out` - Active connections
- `cache_hits_total` - Cache hit count

### Grafana
**URL**: http://localhost:3001  
**Username**: admin  
**Password**: admin123  

**Dashboards**:
1. API Response Time (p95)
2. Request Rate
3. Error Rate
4. Cache Hit Rate
5. Database Connections
6. Business Metrics

### Import Dashboard
```bash
# Manual import in Grafana UI
# 1. Go to Dashboards > Import
# 2. Upload: backend/monitoring/grafana_dashboard.json
# 3. Select Prometheus data source
# 4. Click Import
```

---

## 🚧 Operations & Maintenance

### Database Optimization
```bash
# Check table statistics
psql -U postgres -d mismatch -c "
  SELECT 
    schemaname, 
    tablename, 
    (pg_total_relation_size(schemaname||'.'||tablename) / 1024 / 1024)::int as size_mb
  FROM pg_tables
  ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
  LIMIT 10;
"

# Vacuum and analyze
psql -U postgres -d mismatch -c "VACUUM ANALYZE;"

# Rebuild indexes
psql -U postgres -d mismatch -c "REINDEX DATABASE mismatch;"
```

### Redis Management
```bash
# Monitor Redis
redis-cli monitor

# Check memory usage
redis-cli INFO memory

# Clear cache
redis-cli FLUSHDB

# Monitor key operations
redis-cli --bigkeys
```

### Celery Tasks
```bash
# Start worker
celery -A app.celeryapp worker --loglevel=info

# Start beat scheduler
celery -A app.celeryapp beat --loglevel=info

# Monitor tasks
celery -A app.celeryapp inspect active

# Purge tasks
celery -A app.celeryapp purge
```

---

## 🚪 Troubleshooting

### 1. High Memory Usage
```bash
# Increase connection pool recycle time
# Edit: app/config/database.py
pool_recycle=3600  # Increase from 1800

# Clear Redis cache
redis-cli FLUSHDB
```

### 2. Slow Queries
```bash
# Enable query logging
psql -U postgres -d mismatch -c "ALTER DATABASE mismatch SET log_min_duration_statement = 100;"

# Check slow queries
psql -U postgres -d mismatch -c "
  SELECT query, calls, mean_exec_time 
  FROM pg_stat_statements 
  ORDER BY mean_exec_time DESC 
  LIMIT 10;
"
```

### 3. Rate Limit Issues
```bash
# Check rate limit config
# Edit: app/config/ratelimiter.py

# Increase limits if needed
RATE_LIMITS = {
    'authenticated': '200 per minute',  # Increase from 100
    # ...
}
```

### 4. Redis Connection Issues
```bash
# Test Redis connection
redis-cli -h localhost -p 6379 ping

# Check Redis logs
docker-compose logs redis

# Restart Redis
docker-compose restart redis
```

---

## 📑 Scaling Recommendations

### Horizontal Scaling
- Use Docker Swarm or Kubernetes
- Load balance with Nginx
- Scale backend services independently

### Database Scaling
- Read replicas for high-load scenarios
- Connection pooling with PgBouncer
- Sharding for very large datasets

### Redis Scaling
- Redis Cluster for distributed caching
- Redis Sentinel for high availability
- Multiple DB numbers for isolation

---

## 📓 Backup & Recovery

### Database Backup
```bash
# Full backup
pg_dump -U postgres mismatch > backup_$(date +%Y%m%d).sql

# Restore from backup
psql -U postgres mismatch < backup_20260108.sql
```

### Automated Backups
```bash
# Add to crontab
0 2 * * * pg_dump -U postgres mismatch > /backups/mismatch_$(date +\%Y\%m\%d).sql
```

---

## 👍 Support & Documentation

- **Phase 6 Summary**: `backend/PHASE_6_SUMMARY.md`
- **Completion Report**: `PHASE_6_COMPLETION_REPORT.md`
- **GitHub Repository**: https://github.com/maksimmishakov/mismatch-recruiter
- **Issues**: Create GitHub issue for bugs/features

---

**Next Phase**: Phase 7 - Production Deployment & CI/CD Pipeline
