# MisMatch Recruiter - Deployment Guide

## Stage 1: Pre-Deployment Validation

### 1.1 Code Quality Checks
```bash
# Run all tests
python -m pytest tests/ -v --cov=app --cov-report=html

# Run linting
flake8 app/ services/ middleware/ --max-line-length=100

# Run type checking
mypy app/ services/ middleware/ --ignore-missing-imports
```

### 1.2 Performance Validation
```bash
# Run performance benchmarks
python tests/test_performance.py

# Check build size
cd frontend && npm run build
ls -lh build/
```

### 1.3 Security Scan
```bash
# Check for vulnerabilities
pip-audit
safety check
```

---

## Stage 2: Staging Deployment

### 2.1 Environment Setup
```bash
# Clone to staging
git clone -b feature/job-enrichment-ml-matching .

# Create virtual environment
python -m venv venv_staging
source venv_staging/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install pytest pytest-cov flake8 mypy
```

### 2.2 Database Migration
```bash
# Backup current database
sqlite3 mismatch.db ".backup mismatch_backup_$(date +%Y%m%d_%H%M%S).db"

# Run migrations
alembic upgrade head
```

### 2.3 Service Deployment
```bash
# Start backend
gunicorn --workers=4 --threads=2 --bind 0.0.0.0:5000 app:app

# Start frontend (in separate terminal)
cd frontend
npm install
npm run build
npm run serve
```

### 2.4 Health Checks
```bash
# Check API health
curl http://localhost:5000/health

# Check frontend
curl http://localhost:3000

# Monitor logs
tail -f logs/mismatch.log
```

---

## Stage 3: Load Testing

### 3.1 Setup Load Test Environment
```bash
# Install locust
pip install locust

# Create load test file
cat > locustfile.py << 'LOAD'
from locust import HttpUser, task, between

class MismatchUser(HttpUser):
    wait_time = between(1, 5)
    
    @task(3)
    def match_resume(self):
        self.client.post("/api/match-resume-to-job",
            json={"resume_id": "123", "job_id": "456"})
    
    @task(1)
    def get_candidates(self):
        self.client.get("/api/candidates")
LOAD
```

### 3.2 Run Load Test
```bash
# Start load testing (10,000 users over 5 minutes)
locust -f locustfile.py -u 10000 -r 200 --run-time 5m --headless

# Monitor metrics
# - Response Time
# - Throughput
# - Error Rate
# - Resource Usage
```

### 3.3 Performance Metrics Analysis
- Response time: Should stay < 100ms (99th percentile)
- Error rate: Should be < 0.1%
- Throughput: Should maintain > 1000 req/sec
- Cache hit rate: Should be > 80%

---

## Stage 4: User Acceptance Testing (UAT)

### 4.1 Test Scenarios
1. **Resume Upload & Parsing**
   - Upload PDF resume
   - Verify data extraction
   - Check processing speed

2. **Job Matching**
   - Create test job
   - Run matching algorithm
   - Verify accuracy (95%+ target)

3. **Dashboard Analytics**
   - View metrics
   - Check real-time updates
   - Verify performance data

4. **User Management**
   - Create HR account
   - Configure permissions
   - Test role-based access

### 4.2 UAT Approval
- [ ] HR Director approval
- [ ] Performance metrics verified
- [ ] All test scenarios passed
- [ ] Security scan passed

---

## Stage 5: Production Deployment

### 5.1 Pre-Production Checklist
- [ ] All commits reviewed and approved
- [ ] Staging tests passed
- [ ] Load testing successful
- [ ] UAT approved
- [ ] Database backups created
- [ ] Rollback plan prepared
- [ ] Monitoring configured
- [ ] Alerts set up

### 5.2 Blue-Green Deployment Strategy
```bash
# 1. Prepare green environment
git pull origin feature/job-enrichment-ml-matching
./deploy.sh --environment production-green

# 2. Run smoke tests
./smoke_tests.sh

# 3. Route 10% traffic to green
kubectl patch service mismatch-recruiter \
  -p '{"spec":{"selector":{"version":"green"}}}' \
  -n production --type merge

# 4. Monitor for 30 minutes
# Metrics should remain stable

# 5. Route 50% traffic
kubectl patch service mismatch-recruiter \
  -p '{"spec":{"selector":{"weight":"50"}}}

# 6. Monitor for 1 hour
# All metrics should be within targets

# 7. Route 100% traffic
kubectl patch service mismatch-recruiter \
  -p '{"spec":{"selector":{"version":"green"}}}'

# 8. Decommission blue environment
kubectl delete deployment mismatch-blue -n production
```

### 5.3 Post-Deployment Verification
```bash
# Check services
kubectl get pods -n production
kubectl get svc -n production

# Verify metrics
curl https://api.mismatch-recruiter.com/health

# Check logs
kubectl logs -n production --all-containers=true -l app=mismatch-recruiter --tail=100

# Run regression tests
python tests/test_regression.py
```

---

## Stage 6: Post-Deployment Monitoring

### 6.1 Key Metrics to Monitor
- API Response Time (Target: < 100ms)
- Error Rate (Target: < 0.1%)
- CPU Usage (Target: < 70%)
- Memory Usage (Target: < 80%)
- Database Query Time (Target: < 50ms)
- Cache Hit Rate (Target: > 85%)

### 6.2 Alert Thresholds
- Response Time > 500ms → Alert
- Error Rate > 1% → Critical Alert
- CPU > 85% → Alert
- Memory > 90% → Alert
- Database Down → Critical Alert

### 6.3 Daily Monitoring Tasks
- [ ] Review error logs
- [ ] Check performance metrics
- [ ] Verify cache effectiveness
- [ ] Monitor resource usage
- [ ] Review user feedback

---

## Rollback Procedure

### Emergency Rollback
```bash
# If production has critical issues
kubectl set image deployment/mismatch-recruiter \
  mismatch=mismatch:previous \
  -n production

# Restore database from backup
sqlite3 mismatch.db ".restore mismatch_backup_<timestamp>.db"

# Verify rollback
curl https://api.mismatch-recruiter.com/health

# Investigate issue
# Create incident report
```

---

## Timeline

- **Day 1:** Staging deployment & validation
- **Day 2-3:** Load testing & optimization
- **Day 4:** UAT & approval
- **Day 5:** Production deployment (Blue-Green)
- **Days 6-7:** Monitoring & optimization

---

