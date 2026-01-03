# MisMatch Recruiter - Deployment Runbook

## Quick Reference

### Critical Links
- **GitHub Repository**: https://github.com/maksimisakov/mismatch-recruiter
- **Live Demo**: https://mismatch-recruiter-maksimisakov.amvera.io
- **Admin Dashboard**: https://mismatch-recruiter-maksimisakov.amvera.io/admin-dashboard
- **Documentation**: ./docs/

### Key Documentation Files
1. **DEPLOYMENT_GUIDE.md** - Full deployment procedures
2. **MONITORING_GUIDE.md** - Production monitoring setup
3. **OPTIMIZATION_SUMMARY.md** - Performance improvements
4. **EXECUTION_REPORT.md** - Project completion details

---

## Phase 1: PRE-DEPLOYMENT (Days -2 to -1)

### Checklist
```bash
☐ Review all commits in feature/job-enrichment-ml-matching
☐ Verify all tests pass locally
☐ Update version number
☐ Create release branch
☐ Generate changelog
☐ Notify stakeholders
```

### Commands
```bash
# Review changes
git log main..feature/job-enrichment-ml-matching --oneline | head -20

# Run full test suite
python -m pytest tests/ -v --cov=app

# Create release branch
git checkout -b release/v1.1.0
git merge feature/job-enrichment-ml-matching
```

---

## Phase 2: STAGING DEPLOYMENT (Day 1)

### Estimated Duration: 2-3 hours

```bash
# 1. Deploy to staging
cd /home/ubuntu/mismatch-staging
git fetch origin
git checkout release/v1.1.0

# 2. Run deployment script
bash scripts/deploy_staging.sh

# 3. Activate environment
source venv_staging/bin/activate

# 4. Start services
gunicorn --workers=4 --threads=2 --bind 0.0.0.0:5000 app:app &
cd frontend && npm run serve &

# 5. Verify health
sleep 10
curl http://localhost:5000/health
curl http://localhost:3000

# 6. Run smoke tests
python scripts/smoke_tests.py
```

### Success Criteria
- [ ] API responds to /health
- [ ] Frontend loads
- [ ] All tests pass
- [ ] Performance metrics acceptable
- [ ] No errors in logs

---

## Phase 3: LOAD TESTING (Days 2-3)

### Setup
```bash
# Install load testing tools
pip install locust

# Create load test file
cat > locustfile.py << 'LOAD'
from locust import HttpUser, task, between

class MismatchUser(HttpUser):
    wait_time = between(1, 5)
    
    @task(3)
    def match(self):
        self.client.post("/api/match-resume-to-job",
            json={"resume_id": "123", "job_id": "456"})
    
    @task(1)
    def health(self):
        self.client.get("/health")
LOAD
```

### Execution
```bash
# Start load test: 5,000 users, 200 spawning rate
locust -f locustfile.py \
  -u 5000 -r 200 \
  -t 30m \
  --host=http://staging:5000 \
  --headless
```

### Success Criteria
- [ ] Response time p99 < 500ms
- [ ] Error rate < 1%
- [ ] Throughput stable > 500 req/sec
- [ ] No memory leaks
- [ ] CPU usage < 80%

---

## Phase 4: USER ACCEPTANCE TESTING (Day 4)

### Test Scenarios

#### Scenario 1: Resume Upload
```bash
Test Steps:
1. Login as HR user
2. Upload sample PDF resume
3. Verify parsing
4. Check extracted data

Expected Result: Data extracted correctly in < 5 seconds
```

#### Scenario 2: Job Matching
```bash
Test Steps:
1. Create test job position
2. Run matching algorithm
3. Review match results
4. Verify accuracy

Expected Result: 95%+ accuracy
```

#### Scenario 3: Dashboard
```bash
Test Steps:
1. View analytics dashboard
2. Check real-time metrics
3. Export reports
4. Verify permissions

Expected Result: All features working, proper access control
```

### Sign-Off
Obtain approval from:
- [ ] HR Director
- [ ] Product Manager
- [ ] QA Lead
- [ ] Engineering Manager

---

## Phase 5: PRODUCTION DEPLOYMENT (Day 5)

### Pre-Deployment Checks
```bash
# 1. Create database backups
cd /home/ubuntu/mismatch-prod
sqlite3 mismatch.db \
  ".backup mismatch_backup_$(date +%Y%m%d_%H%M%S).db"

# 2. Verify current metrics
curl https://api.mismatch-recruiter.com/health/detailed

# 3. Check disk space
df -h

# 4. Verify monitoring is active
kubectl get pods -n production -l app=mismatch-recruiter
```

### Deployment (Blue-Green Strategy)

```bash
# 1. Prepare green environment
git pull origin release/v1.1.0
bash scripts/deploy_staging.sh

# 2. Run smoke tests
python scripts/smoke_tests.py
echo "Smoke tests: $?"

# 3. Route 10% traffic
kubectl patch service mismatch-recruiter \
  -p '{"spec":{"selector":{"version":"green"}}}' \
  --record -n production

echo "Waiting 30 minutes..."
sleep 1800

# 4. Monitor metrics
echo "Checking metrics..."
curl https://api.mismatch-recruiter.com/health/detailed

# 5. Route 50% traffic
kubectl patch service mismatch-recruiter \
  -p '{"spec":{"selector":{"weight":"50"}}}' \
  -n production --record

echo "Waiting 1 hour..."
sleep 3600

# 6. Route 100% traffic
kubectl patch service mismatch-recruiter \
  -p '{"spec":{"selector":{"version":"green"}}}' \
  -n production --record

echo "Waiting 30 minutes for stabilization..."
sleep 1800

# 7. Verify production
curl https://api.mismatch-recruiter.com/health

# 8. Cleanup blue environment
kubectl delete deployment mismatch-blue -n production
```

### Post-Deployment Verification
```bash
# Check pod status
kubectl get pods -n production

# Check logs for errors
kubectl logs -n production \
  -l app=mismatch-recruiter \
  --tail=50 --all-containers=true

# Verify metrics
curl https://api.mismatch-recruiter.com/metrics

# Run regression tests
python tests/test_regression.py
```

---

## Phase 6: POST-DEPLOYMENT MONITORING (Days 6-7)

### Daily Tasks
```bash
# Morning standup check
echo "=== Production Status ==="
kubectl get pods -n production
kubectl top pods -n production

# Check error logs
kubectl logs -n production \
  -l app=mismatch-recruiter \
  --since=24h | grep ERROR

# Review metrics
echo "Current metrics:"
curl https://api.mismatch-recruiter.com/health/detailed

# Check alerts
echo "Active alerts:"
kubectl get alerts -n production
```

### Metrics to Monitor
- API Response Time: Should be < 100ms (p99)
- Error Rate: Should be < 0.1%
- CPU Usage: Should be < 60%
- Memory Usage: Should be < 70%
- Database Connections: Should be < 80% of max
- Cache Hit Rate: Should be > 85%

---

## ROLLBACK PROCEDURE (If Issues)

### Immediate Rollback
```bash
# 1. Switch traffic back to blue
kubectl patch service mismatch-recruiter \
  -p '{"spec":{"selector":{"version":"blue"}}}' \
  -n production --record

# 2. Restore database from backup
sqlite3 mismatch.db \
  ".restore mismatch_backup_20250103_123456.db"

# 3. Verify rollback
curl https://api.mismatch-recruiter.com/health

# 4. Alert team
echo "ROLLBACK INITIATED - Check Slack #incidents"
```

### Investigation
```bash
# 1. Gather logs
kubectl logs -n production \
  -l app=mismatch-recruiter \
  --since=1h > incident_logs.txt

# 2. Check metrics at time of failure
prometheus query 'rate(errors_total[5m])' --start 20250103T150000 --end 20250103T160000

# 3. Create incident report
echo "Incident Report
  - Time: $(date)
  - Impact: Production outage
  - Duration: XX minutes
  - Root Cause: TBD
  - Resolution: Rollback to previous version" > incident_report.txt
```

---

## CONTACTS & ESCALATION

```
SEV-1 Incident:
  - On-Call Engineer: dev-oncall@company.com
  - Engineering Manager: manager@company.com
  - VP Engineering: vp@company.com
  - Emergency Line: +1-XXX-XXX-XXXX

SEV-2 Issue:
  - On-Call Engineer: dev-oncall@company.com
  - Team Lead: lead@company.com

SEV-3 Issue:
  - On-Call Engineer: dev-oncall@company.com
```

---

## SUCCESS METRICS

Deployment is considered successful when:
- ✅ All pods are running and healthy
- ✅ API response time < 100ms (p99)
- ✅ Error rate < 0.1%
- ✅ Zero data loss
- ✅ Users report normal operation
- ✅ No critical alerts fired
- ✅ Performance metrics within targets

---

**Deployment Date**: [To be scheduled]
**Deployed By**: [Engineer name]
**Approved By**: [Manager name]
**Status**: 🚀 Ready for Production

