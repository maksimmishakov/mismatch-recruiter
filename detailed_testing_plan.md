# 🎯 DETAILED TESTING PLAN - MISMATCH RECRUITER
## Complete 16-Hour Testing Framework (January 8-12, 2026)

---

## PHASE 1: LOAD & STRESS TESTING (Monday-Tuesday, 8-9 Jan)
### Total Time: 6 hours

### ШАГ 1.1: Install Locust
```bash
pip install locust==2.24.0
mkdir performance_tests && cd performance_tests
locust --version
```

### ШАГ 1.2: Create locustfile.py
```python
from locust import HttpUser, task, between, events
import json
import time

class MismatchUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        # Login
        response = self.client.post("/api/v1/auth/login", json={
            "email": "test@example.com",
            "password": "password123"
        })
        self.token = response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}
    
    @task(10)
    def get_candidates(self):
        self.client.get("/api/v1/candidates?page=1&limit=20", 
                       headers=self.headers)
    
    @task(8)
    def search_matches(self):
        self.client.post("/api/v1/matching/search", 
                        json={"job_id": "123", "limit": 10},
                        headers=self.headers)
    
    @task(2)
    def create_candidate(self):
        self.client.post("/api/v1/candidates",
                        json={
                            "email": f"test{time.time()}@example.com",
                            "name": "Test User",
                            "resume": "Sample resume"
                        },
                        headers=self.headers)

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    print("\n=== LOAD TEST RESULTS ===")
    print(f"Requests/sec: {environment.stats.total.avg_response_time}")
```

### ШАГ 1.3: Run Load Test (1000 VU)
```bash
locust -f locustfile.py \
  --host http://localhost:5000 \
  --users 1000 \
  --spawn-rate 50 \
  --run-time 30m \
  --headless \
  --csv=results
```

**Acceptance Criteria:**
- ✅ P99 < 500ms
- ✅ Error rate < 1%
- ✅ Success rate > 99%

### ШАГ 1.4: Stress Test
```bash
locust -f locustfile.py \
  --host http://localhost:5000 \
  --users 5000 \
  --spawn-rate 100 \
  --run-time 15m \
  --headless
```

**Goal:** Find breaking point

### ШАГ 1.5: Spike Test
```bash
# 100 VU (5 min) → 500 VU (2 min) → 100 VU (3 min)
# Validate recovery time
```

### ШАГ 1.6: Endurance Test
```bash
locust -f locustfile.py \
  --host http://localhost:5000 \
  --users 200 \
  --run-time 1h \
  --headless
```

**Monitor:** Memory leaks, connection exhaustion

---

## PHASE 2: SECURITY AUDIT (Monday-Tuesday)
### Total Time: 2 hours

### ШАГ 2.1: SQL Injection Testing
```bash
pip install sqlmap

sqlmap -u "http://localhost:5000/api/v1/candidates?page=1&limit=20" \
  --headers "Authorization: Bearer YOUR_TOKEN" \
  --batch \
  --technique=BEUSTQ
```

**Expected Result:** "No vulnerabilities found"

### ШАГ 2.2: XSS Testing
```python
# xss_test.py
import requests

payloads = [
    '<script>alert("XSS")</script>',
    '"><script>alert(String.fromCharCode(88,83,83))</script>',
    '<img src=x onerror=alert("XSS")>',
    '<svg onload=alert("XSS")>'
]

for payload in payloads:
    response = requests.post(
        "http://localhost:5000/api/v1/candidates",
        json={"name": payload},
        headers={"Authorization": "Bearer token"}
    )
    # Should return 400 Bad Request or escaped payload
    assert response.status_code in [400, 200]
```

### ШАГ 2.3: CORS Verification
```bash
curl -i -X OPTIONS http://localhost:5000/api/v1/candidates \
  -H "Origin: http://attacker.com" \
  -H "Access-Control-Request-Method: POST"

# Should show: Access-Control-Allow-Origin: http://localhost:3000
# NOT: Access-Control-Allow-Origin: *
```

### ШАГ 2.4: Rate Limiting
```python
import requests
import time

for i in range(10):
    response = requests.post(
        "http://localhost:5000/api/v1/auth/login",
        json={"email": "test@example.com", "password": "password"}
    )
    print(f"Request {i}: {response.status_code}")
    if i >= 5:
        assert response.status_code == 429, "Should rate limit after 5 attempts"
    time.sleep(0.1)
```

### ШАГ 2.5: JWT Authentication
```python
# Test cases:
# 1. No token → 401
# 2. Wrong token → 401
# 3. Modified token → 401
# 4. Expired token → 401
```

---

## PHASE 3: E2E TESTING (Wednesday-Thursday, 10-11 Jan)
### Total Time: 3 hours

### ШАГ 3.1: Install Playwright
```bash
cd frontend
npm install -D @playwright/test
npx playwright install
```

### ШАГ 3.2: Create E2E Tests

**tests/auth.spec.ts**
```typescript
import { test, expect } from '@playwright/test';

const BASE_URL = 'http://localhost:3000';

test('should register new user', async ({ page }) => {
  await page.goto(`${BASE_URL}/register`);
  await page.fill('input[name="email"]', `test${Date.now()}@example.com`);
  await page.fill('input[name="password"]', 'SecurePassword123!@#');
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL(`${BASE_URL}/dashboard`);
});

test('should login user', async ({ page }) => {
  await page.goto(`${BASE_URL}/login`);
  await page.fill('input[name="email"]', 'test@example.com');
  await page.fill('input[name="password"]', 'password123');
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL(`${BASE_URL}/dashboard`);
});
```

### ШАГ 3.3: Run E2E Tests
```bash
npx playwright test
npx playwright show-report
```

**Success Criteria:**
- ✅ 100% pass rate
- ✅ < 10 minutes runtime
- ✅ Zero flaky tests

---

## PHASE 4: DOCUMENTATION REVIEW (Wednesday-Thursday)
### Total Time: 2 hours

### Checklist:
- [ ] API.md complete with all endpoints
- [ ] ARCHITECTURE.md with diagrams
- [ ] DEPLOYMENT.md with runbooks
- [ ] INSTALLATION.md updated
- [ ] README.md clear and accurate

---

## PHASE 5: FINAL CHECKS & DEMO (Friday, 12 Jan)
### Total Time: 4 hours

### ШАГ 5.1: System Warmup
```bash
# Check all services
docker-compose ps

# Health checks
curl http://localhost:5000/health
curl http://localhost:3000

# Database ready
psql -U user -d mismatch -c "SELECT COUNT(*) FROM candidates;"
```

### ШАГ 5.2: Demo Scenarios

**Scenario 1: Dashboard (3 min)**
- Login
- Show KPI cards
- Display candidates list

**Scenario 2: Matching (5 min)**
- Select job
- Run "Find Matches"
- Show results with scores

**Scenario 3: Performance (3 min)**
- Show metrics: P99=300ms, 1000 VU, 99.5% success

**Scenario 4: AI Accuracy (2 min)**
- Explain matching algorithm
- Show feedback mechanism
- Metric: 92% accuracy

### ШАГ 5.3: Final Sanity Checks
```bash
# Run final check script
bash demo_scripts/final_check.sh

# Verify:
# ✅ Backend health
# ✅ Frontend loading
# ✅ Database OK
# ✅ Redis OK
# ✅ Sample data > 100 candidates
# ✅ API endpoints responding
# ✅ Performance OK (100 concurrent)
```

---

## 📊 SUCCESS GATES (GO/NO-GO)

### ✅ GO CRITERIA:
- P99 latency < 500ms (preferably < 300ms)
- Error rate < 1%
- Handles 1000+ concurrent users
- Zero critical security vulnerabilities
- All E2E tests pass (100%)
- System stable for 1+ hour under load

### ❌ NO-GO CRITERIA:
- Any SQL injection vulnerability
- Any XSS vulnerability
- P99 > 1000ms
- Error rate > 5%
- E2E test fail rate > 10%
- System crashes during load test

---

## TIMELINE SUMMARY

| Day | Phase | Hours | Status |
|-----|-------|-------|--------|
| Mon-Tue | Load Testing | 3 | Pending |
| Mon-Tue | Security Audit | 2 | Pending |
| Wed-Thu | E2E Testing | 3 | Pending |
| Wed-Thu | Documentation | 2 | Pending |
| Fri | Final Checks | 4 | Pending |
| **TOTAL** | | **16h** | **Ready** |

---

**Created:** January 1, 2026
**Status:** Ready for Execution
**Target:** Lamoda Integration
