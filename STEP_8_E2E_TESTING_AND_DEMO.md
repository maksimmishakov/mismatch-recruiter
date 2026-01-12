# STEP 8: E2E TESTING & DEMO PREPARATION

**Status:** Ready for Execution
**Date:** January 12, 2026
**Timeline:** 2-3 hours
**Target:** Full E2E test suite passing + Demo data ready

## STEP 8.1: E2E Testing Framework

### What is E2E Testing?

End-to-End (E2E) testing verifies the entire application workflow:
- User registration → Login → Data operations → Matching algorithm
- API endpoints working correctly
- Database persistence
- Error handling

### E2E Test Architecture

```
Test Flow:
HEALTH CHECK (API Ready?)
    ↓
USER SIGNUP (Registration Works?)
    ↓
GET CANDIDATES (CRUD Read Works?)
    ↓
CREATE CANDIDATE (CRUD Create Works?)
    ↓
CREATE JOB (Job posting Works?)
    ↓
RUN MATCHING (Algorithm Works?)
    ↓
✅ ALL E2E TESTS PASSED
```

## STEP 8.2: Pre-E2E Local Verification

Before running E2E tests against staging, verify locally:

```bash
# 1. Run local unit tests
pytest -v
# EXPECTED: 10/10 passing

# 2. Verify API health locally
python -c "from app import create_app; app = create_app(); print('App created successfully')"
# EXPECTED: App created successfully

# 3. Check Git status
git status
# EXPECTED: nothing to commit, working tree clean
```

## STEP 8.3: E2E Test Checklist

These tests MUST pass before demo:

- [ ] Test 1: Health Endpoint
  - API is running and responding
  - Status: 200 OK
  - Response: `{"status": "ok"}`

- [ ] Test 2: User Registration/Login
  - User can register with email/password
  - User receives authentication token
  - Token is valid JWT

- [ ] Test 3: Candidate CRUD
  - Can retrieve list of candidates
  - Can create new candidate
  - Candidate data persists

- [ ] Test 4: Job CRUD
  - Can retrieve list of jobs
  - Can create new job posting
  - Job data persists

- [ ] Test 5: Matching Algorithm
  - Can trigger matching for a job
  - Returns list of matched candidates
  - Match scores are calculated correctly

- [ ] Test 6: Data Consistency
  - Data survives service restart
  - No data loss between requests
  - Database is persistent

## STEP 8.4: E2E Testing Against Local App

For quick E2E testing without Amvera:

```bash
# 1. Start app locally
python -m flask run --port 5000

# In another terminal:

# 2. Run health check
curl http://localhost:5000/api/health

# 3. Register user
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "Test123!"}'

# 4. Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "Test123!"}'

# 5. Get candidates
curl http://localhost:5000/api/candidates

# 6. Create candidate
curl -X POST http://localhost:5000/api/candidates \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"name": "John Doe", "skills": ["Python", "Django"]}'

# 7. Create job
curl -X POST http://localhost:5000/api/jobs \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"title": "Senior Developer", "required_skills": ["Python"]}'

# 8. Run matching
curl -X POST http://localhost:5000/api/jobs/1/match \
  -H "Authorization: Bearer <token>"
```

## STEP 8.5: Demo Data Preparation

### Demo Data Requirement

For successful demo, prepare:
- 3+ Sample candidates with diverse skills
- 3+ Sample job postings
- Pre-calculated matches to show
- Demo user account for live demo

### Demo Data Script

Create `scripts/create_demo_data.py`:

```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')
from app import create_app, db
from app.models import User, Candidate, JobPosting
from datetime import datetime

app = create_app()

with app.app_context():
    # Clear existing data
    Candidate.query.delete()
    JobPosting.query.delete()
    
    # Create demo candidates
    candidates = [
        Candidate(
            first_name='Alexey',
            last_name='Petrov',
            email='alexey@lamoda.tech',
            experience_years=7,
            skills_text='Python,Django,PostgreSQL,Docker',
            languages_text='Russian,English'
        ),
        Candidate(
            first_name='Maria',
            last_name='Volkova',
            email='maria@lamoda.tech',
            experience_years=5,
            skills_text='Python,FastAPI,PostgreSQL,AWS',
            languages_text='Russian,English,German'
        ),
        Candidate(
            first_name='Ivan',
            last_name='Sokolov',
            email='ivan@lamoda.tech',
            experience_years=3,
            skills_text='JavaScript,React,PostgreSQL,Node.js',
            languages_text='Russian,English'
        )
    ]
    db.session.add_all(candidates)
    
    # Create demo jobs
    jobs = [
        JobPosting(
            title='Senior Python Developer',
            description='Building e-commerce backend for Lamoda',
            required_skills_text='Python,Django,PostgreSQL',
            salary_range='250000-350000 RUB',
            location='Moscow'
        ),
        JobPosting(
            title='Full Stack Developer',
            description='Full stack development for Lamoda mobile app',
            required_skills_text='Python,JavaScript,React,PostgreSQL',
            salary_range='220000-300000 RUB',
            location='Moscow'
        ),
        JobPosting(
            title='DevOps Engineer',
            description='Infrastructure and deployment for Lamoda',
            required_skills_text='Docker,Python,AWS,PostgreSQL',
            salary_range='300000-400000 RUB',
            location='Moscow'
        )
    ]
    db.session.add_all(jobs)
    db.session.commit()
    
    print(f"✅ Created {len(candidates)} demo candidates")
    print(f"✅ Created {len(jobs)} demo jobs")
    print(f"✅ Demo data ready for demonstration")
```

### Run Demo Data Script

```bash
# Prepare demo data locally
python scripts/create_demo_data.py
# EXPECTED OUTPUT:
# ✅ Created 3 demo candidates
# ✅ Created 3 demo jobs
# ✅ Demo data ready for demonstration
```

## STEP 8.6: Demo Scenario Flow

For LAMODA presentation (Jan 15, 14:00 MSK):

### Part 1: Infrastructure Overview (2 min)
- Show GitHub repository
- Explain tech stack
- Highlight key features

### Part 2: API Demo (3 min)
1. Health check: API is running
   ```bash
   curl $STAGING_URL/api/health
   ```

2. Show candidate list: Data is loaded
   ```bash
   curl $STAGING_URL/api/candidates
   ```

3. Create candidate: Real-time data entry
   ```bash
   curl -X POST $STAGING_URL/api/candidates ...
   ```

### Part 3: Matching Algorithm (3 min)
1. Run matching for job ID 1
2. Show matched candidates
3. Explain scoring algorithm
4. Discuss accuracy improvements

### Part 4: Q&A (2 min)
- Answer technical questions
- Discuss timeline
- Next steps

## STEP 8.7: Final Verification Before Demo

```bash
# 1 hour before demo:

# Verify all systems online
echo "Checking systems..."

# Health check
curl -s $STAGING_URL/api/health | jq .

# Test authentication
curl -X POST $STAGING_URL/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "demo@lamoda.tech", "password": "...'"}'

# Verify demo data exists
curl -s $STAGING_URL/api/candidates | jq '.candidates | length'

# Test matching
curl -s -X POST $STAGING_URL/api/jobs/1/match \
  -H "Authorization: Bearer $TOKEN" | jq .

echo "✅ All systems ready for demo"
```

## STEP 8.8: Troubleshooting During Demo

### If API is slow:
- Wait 3-5 seconds (cold start)
- Check Amvera logs
- Restart application from dashboard

### If endpoint returns 404:
- Check URL spelling
- Verify authentication token
- Check Amvera logs for route issues

### If database is empty:
- Run demo data script again
- Check database is connected
- Verify persistence (restart app, check data still there)

### If matching fails:
- Verify candidates exist
- Verify job exists
- Check matching algorithm logs
- Fall back to static demo results

## STEP 8.9: Success Criteria

### MUST HAVE (for successful demo):
- ✅ Health endpoint returns 200 OK
- ✅ API responds in <1 second
- ✅ Demo data loads successfully
- ✅ At least 2 API endpoints work
- ✅ No errors in Amvera logs

### NICE TO HAVE:
- ✅ Matching algorithm returns results
- ✅ Live data creation during demo
- ✅ Database persistence demonstrated
- ✅ Error handling shown

## STEP 8.10: Post-Demo Checklist

- [ ] Demo completed successfully
- [ ] Feedback captured
- [ ] Notes taken on improvements
- [ ] Next meeting scheduled
- [ ] Repository updated with learnings

---

**Generated:** January 12, 2026
**Status:** Ready for E2E Testing
