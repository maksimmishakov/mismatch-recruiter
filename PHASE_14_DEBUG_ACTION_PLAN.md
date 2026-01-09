# Phase 14: Backend Debug & Production Validation - Action Plan

**Date**: January 9, 2026, 20:00 MSK  
**Status**: PHASE 14 IN PROGRESS
**Focus**: Backend ImportError Resolution & Infrastructure Validation

---

## Current Findings (Session Investigation)

### Problem Identified
**ImportError in Config Module**
```
ImportError: cannot import name 'Config' from 'app.config' (unknown location). Did you mean: 'config'?
```

**Root Cause Analysis**:
- File path: `backend/app/config/__init__.py`
- Issue: The `Config` class is not being properly exported from the config module
- Evidence: Error traceback shows import failure on line 5 of backend/app/__init__.py
- Location: `/workspaces/mismatch-recruiter/backend/app/config/` directory contains 12 config files but no proper Config class export

### Config Module Structure Found
Files in `backend/app/config/`:
- `__init__.py` - Package initialization (needs inspection)
- `__pycache__` - Python cache
- `celery_config.py` - Celery configuration
- `database.py` - Database configuration
- `development.py` - Development config
- `metrics.py` - Metrics configuration
- `production.py` - Production config
- `ratelimiter.py` - Rate limiter config
- `redis.py` - Redis configuration
- `staging.py` - Staging config
- `testing.py` - Test configuration

---

## Resolution Strategy

### Step 1: Fix Config Module Export (PRIORITY: CRITICAL)

**Option A: Update backend/app/config/__init__.py** (Recommended)
```python
# backend/app/config/__init__.py
from .development import Config as DevelopmentConfig
from .production import Config as ProductionConfig
from .testing import Config as TestingConfig
from .staging import Config as StagingConfig

# Export appropriate config based on environment
import os

ENV = os.getenv('FLASK_ENV', 'development')

if ENV == 'production':
    Config = ProductionConfig
elif ENV == 'testing':
    Config = TestingConfig
elif ENV == 'staging':
    Config = StagingConfig
else:
    Config = DevelopmentConfig

__all__ = ['Config', 'DevelopmentConfig', 'ProductionConfig', 'TestingConfig', 'StagingConfig']
```

**Option B: Fix Import Statement in backend/app/__init__.py**
```python
# Instead of:
from app.config import Config

# Use one of:
from app.config.development import Config  # For development
from app.config.production import Config   # For production
from app.config import Config  # Once __init__.py is fixed
```

### Step 2: Environment Variable Configuration

Ensure `.env` file contains:
```bash
FLASK_ENV=development  # or production/staging
FLASK_APP=backend.app
DATABASE_URL=postgresql://mismatch_user:mismatch_password@postgres:5432/mismatch_db
REDIS_URL=redis://redis:6379/0
SECRET_KEY=your-secret-key-here
```

### Step 3: Docker Container Rebuild

```bash
# Rebuild backend image with fixed code
docker-compose build backend

# Restart backend service
docker-compose up -d backend

# Verify startup
docker logs -f mismatch-recruiter-backend
```

### Step 4: Verification Tests

```bash
# Test 1: Python import in isolation
python3 -c "from backend.app.config import Config; print('✅ Config import successful')"

# Test 2: Health endpoint
curl http://localhost:5000/api/health

# Test 3: Container logs
docker logs mismatch-recruiter-backend | grep -E "(ERROR|WARNING|Running on)"
```

---

## Complete Debug Checklist

### Phase 14.1: Backend Fix (TODAY)
- [ ] Review all config/*.py files for Config class definitions
- [ ] Create proper __init__.py with Config export
- [ ] Test config import locally
- [ ] Rebuild Docker container
- [ ] Verify backend starts without errors
- [ ] Test API health endpoint (GET /api/health)
- [ ] Check database connectivity
- [ ] Verify Redis connection

### Phase 14.2: API Validation (TODAY)
- [ ] Test all candidate endpoints
- [ ] Test all job endpoints
- [ ] Test authentication endpoints
- [ ] Verify error handling
- [ ] Check API response times
- [ ] Validate JSON schema

### Phase 14.3: Load Testing (TODAY)
- [ ] Prepare load test environment
- [ ] Run baseline performance test (100 users, 5 minutes)
- [ ] Record metrics: RPS, latency p95/p99, errors
- [ ] Verify database handles concurrent connections
- [ ] Check memory usage under load

### Phase 14.4: Security Validation (TODAY)
- [ ] Run Bandit security scan
- [ ] Check dependencies for vulnerabilities (Safety)
- [ ] Verify SSL/TLS configuration
- [ ] Test SQL injection protection
- [ ] Test XSS protection
- [ ] Verify authentication & authorization

### Phase 14.5: Integration Testing (TOMORROW)
- [ ] Run pytest integration tests
- [ ] Run API contract tests
- [ ] Database migration tests
- [ ] Cache functionality tests
- [ ] Background job tests (Celery)

---

## Expected Outcomes

**After Implementing Step 1-3:**
- ✅ Backend container starts successfully
- ✅ No ImportError in logs
- ✅ API responds to health checks
- ✅ Database connectivity confirmed
- ✅ Redis cache operational

**Production Readiness Signs:**
- ✅ All API endpoints respond with 200 OK
- ✅ Response time p95 < 100ms
- ✅ Error rate < 0.1%
- ✅ No security vulnerabilities found
- ✅ Load test passing 1000 req/sec
- ✅ All integration tests passing

---

## Troubleshooting Guide

### If Backend Still Fails After Fix

**Check 1: Verify config files exist**
```bash
ls -la backend/app/config/*.py
```

**Check 2: Test config import directly**
```bash
python3 << 'EOF'
import sys
sys.path.insert(0, 'backend')
try:
    from app.config import Config
    print(f"✅ Config: {Config}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
EOF
```

**Check 3: Verify environment variables**
```bash
env | grep -E "(FLASK|DATABASE|REDIS)"
```

**Check 4: Docker container examination**
```bash
docker exec mismatch-recruiter-backend python3 -c "from app.config import Config; print('Config OK')"
```

---

## Timeline & Next Steps

**Immediate (Next 2 Hours)**:
1. Fix config __init__.py
2. Rebuild Docker image
3. Verify import works
4. Test API endpoints

**Today (By 18:00 MSK)**:
- Phase 14.1 & 14.2 complete
- Baseline performance metrics recorded
- Security scan results available

**Tomorrow (January 10)**:
- Phase 14.3, 14.4, 14.5 complete
- Final production readiness verification
- Go/No-Go decision for pilot deployment

---

## Success Criteria

✅ **Phase 14 Complete When:**
1. ImportError resolved & backend operational
2. All API endpoints responding correctly
3. Load test baseline established (> 1000 req/sec)
4. Security scan passed (0 critical vulnerabilities)
5. Integration tests 100% passing
6. Production readiness checklist: 100% green
7. Team sign-off for pilot deployment

---

**Document Status**: ACTIVE - In Development  
**Last Updated**: January 9, 2026, 20:30 MSK  
**Owner**: Maksim Mishakov  
**Escalation**: Tech Lead
