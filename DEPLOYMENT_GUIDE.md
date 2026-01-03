# MisMatch Recruiter - Production Deployment Guide

## System Requirements

- **OS:** Linux (Ubuntu 20.04+ recommended)
- **Python:** 3.10+
- **Node.js:** 18.x LTS
- **PostgreSQL:** 13+
- **Redis:** 6+
- **Memory:** 4GB minimum (8GB recommended)
- **Storage:** 20GB minimum
- **Network:** Stable internet connection

## Pre-Deployment Checklist

- [ ] All 4 scientific innovations tested locally
- [ ] API endpoints verified working
- [ ] Database optimized and backed up
- [ ] Environment variables configured
- [ ] SSL/TLS certificates ready
- [ ] CDN configured (optional)
- [ ] Monitoring and alerting setup
- [ ] Backup strategy verified

## Deployment Steps

### 1. Infrastructure Setup (Amvera)

```bash
# Create new deployment on Amvera
git push origin main

# Amvera automatically detects and builds
# - Builds Docker image
# - Runs database migrations
# - Installs dependencies
# - Starts services
```

### 2. Environment Configuration

Create `.env.production`:
```
FLASK_ENV=production
DEBUG=false
DATABASE_URL=postgresql://user:password@host:5432/mismatch
REDIS_URL=redis://localhost:6379/0
OPENAI_API_KEY=sk-...
JWT_SECRET=your-secret-key
LOG_LEVEL=INFO
```

### 3. Database Setup

```bash
# Run migrations
flask db upgrade

# Create indices
python scripts/create_indices.py

# Initialize cache
python scripts/warmup_cache.py
```

### 4. Performance Tuning

```bash
# PostgreSQL optimization
# Edit postgresql.conf:
shared_buffers = 2GB
effective_cache_size = 6GB
work_mem = 50MB

# Redis configuration
maxmemory = 2gb
maxmemory-policy = allkeys-lru
```

### 5. Service Startup

```bash
# Start Flask backend
gunicorn app:app --workers 4 --worker-class gevent

# Start frontend
npm run build && npm run start

# Start monitoring
python monitoring/metrics_collector.py
```

### 6. Health Check

```bash
# Verify all services
curl http://localhost:3000/api/health

# Expected response:
# {"status": "OK", "uptime": 99.9, ...}
```

## Post-Deployment

### Monitoring
- Monitor real-time metrics via WebSocket
- Set up alerting for downtime
- Check system health regularly

### Backup
- Daily database backups
- Weekly full system snapshots
- Offsite backup storage

### Updates
- Schedule maintenance windows
- Test updates in staging first
- Keep dependencies current

## Performance Targets

- **Uptime:** 99.9%
- **Response Time:** <50ms average
- **Throughput:** 1000+ req/sec
- **Latency:** <100ms p95
- **CPU Usage:** <80%
- **Memory Usage:** <80%

## Troubleshooting

### High Response Times
- Check database query performance
- Verify cache is working
- Monitor CPU and memory usage

### Database Connection Issues
- Verify connection string
- Check network connectivity
- Review PostgreSQL logs

### API Errors
- Check error logs
- Verify all services are running
- Test individual endpoints

