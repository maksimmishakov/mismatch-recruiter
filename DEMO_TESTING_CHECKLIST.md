# MisMatch Recruiter - DEMO TESTING CHECKLIST

**Date:** January 7, 2026
**Demo Date:** January 8, 2026 at 13:00 MSK
**Status:** 🟢 READY FOR TESTING

---

## 📝 PRE-DEMO TESTING CHECKLIST

### Phase 1: Environment Setup (5 minutes)

- [ ] **Step 1:** Clear all old containers and volumes
```bash
docker-compose down -v
```

- [ ] **Step 2:** Rebuild all Docker images
```bash
docker-compose build --no-cache
```

- [ ] **Step 3:** Start all services
```bash
docker-compose up
```

- [ ] **Step 4:** Wait for all services to start (should see "Running on http://0.0.0.0:5000")

---

### Phase 2: API Health Check (2 minutes)

In a new terminal:

```bash
# Test 1: Health Check
curl http://localhost:5000/api/health
# Expected: {"status": "ok"}

# Test 2: Register User
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@lamoda.com","password":"demo123","username":"demolamoda"}'
# Expected: {"user_id": 1}

# Test 3: Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@lamoda.com","password":"demo123"}'
# Expected: {"access_token": "eyJ..."}
```

---

### Phase 3: Core CRUD Operations (5 minutes)

**Save the access_token from login response for the following tests:**

```bash
TOKEN="<paste_your_access_token_here>"
```

#### Candidates API

```bash
# Create Candidate
curl -X POST http://localhost:5000/api/candidates \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Ivan",
    "last_name": "Petrov",
    "email": "ivan.petrov@lamoda.com",
    "skills": ["Python", "Flask", "Docker"],
    "experience_years": 5
  }'
# Expected: {"id": 1, ...}

# Get All Candidates
curl http://localhost:5000/api/candidates
# Expected: [...list of candidates...]

# Get Single Candidate (replace 1 with actual ID)
curl http://localhost:5000/api/candidates/1
# Expected: {"id": 1, "first_name": "Ivan", ...}

# Update Candidate
curl -X PUT http://localhost:5000/api/candidates/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"skills": ["Python", "Flask", "Docker", "Kubernetes"]}'
# Expected: {"message": "Candidate updated", ...}
```

#### Jobs API

```bash
# Create Job
curl -X POST http://localhost:5000/api/jobs \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Senior Python Developer",
    "description": "We are looking for a senior Python developer for our team",
    "company": "Lamoda",
    "location": "Moscow",
    "required_skills": ["Python", "Flask", "Docker"],
    "experience_level": "senior"
  }'
# Expected: {"id": 1, ...}

# Get All Jobs
curl http://localhost:5000/api/jobs
# Expected: [...list of jobs...]

# Get Single Job (replace 1 with actual ID)
curl http://localhost:5000/api/jobs/1
# Expected: {"id": 1, "title": "Senior Python Developer", ...}
```

#### Matches API

```bash
# Create Match (between candidate 1 and job 1)
curl -X POST http://localhost:5000/api/matches \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": 1,
    "job_posting_id": 1,
    "match_score": 0.85,
    "skill_match": 0.9,
    "experience_match": 0.8
  }'
# Expected: {"message": "Match created", "match": {...}}

# Get All Matches
curl http://localhost:5000/api/matches
# Expected: [...list of matches...]
```

---

### Phase 4: Frontend Verification (2 minutes)

```bash
# Open in browser:
http://localhost:3000

# You should see:
# - "MisMatch Recruiter" title
# - API Status indicator (should say "API is healthy")
# - Registration form
# - Ability to register new user
```

---

## ✅ SUCCESS CRITERIA

All of the following must pass:

- [ ] Docker containers start without errors
- [ ] Backend API is accessible on http://localhost:5000
- [ ] Health check endpoint responds with status "ok"
- [ ] User registration works (creates user)
- [ ] User login works (returns JWT token)
- [ ] All 15+ API endpoints respond correctly
- [ ] Candidates CRUD operations work
- [ ] Jobs CRUD operations work
- [ ] Matches CRUD operations work
- [ ] Frontend loads on http://localhost:3000
- [ ] Frontend shows API health status
- [ ] No errors in console logs

---

## 🚫 TROUBLESHOOTING

If something fails:

### Error: Port already in use
```bash
sudo lsof -i :5000
sudo kill -9 <PID>

sudo lsof -i :3000
sudo kill -9 <PID>

sudo lsof -i :5432
sudo kill -9 <PID>
```

### Error: Database connection failed
```bash
# Wait 10 seconds for PostgreSQL to start
sleep 10

# Check database logs
docker-compose logs db
```

### Error: Backend won't start
```bash
# Check backend logs
docker-compose logs backend

# Rebuild without cache
docker-compose build --no-cache
```

### Error: 502 Bad Gateway
```bash
# Backend is not responding, check:
docker-compose ps

# Restart services
docker-compose restart backend
```

---

## 📑 DEMO TALKING POINTS

1. **Architecture:** Modern Flask backend + React frontend + PostgreSQL
2. **API Design:** RESTful with JWT authentication
3. **Features:** Full CRUD for candidates, jobs, and matches
4. **Matching Algorithm:** Skill-based and experience-based scoring
5. **Infrastructure:** Docker containerization for easy deployment
6. **CI/CD:** GitHub Actions for automated testing
7. **Scalability:** Ready for horizontal scaling

---

## 🏃 QUICK START FOR DEMO

```bash
# 1. Terminal 1: Start services
cd /path/to/mismatch-recruiter
docker-compose down -v
docker-compose up

# 2. Terminal 2: Run test commands (see Phase 2-3 above)
# 3. Browser: Open http://localhost:3000 to show frontend
```

**Expected Demo Duration:** 10-15 minutes

---

## 🙋 SUPPORT CONTACTS

- **Technical Issues:** Check CRITICAL_FIXES_APPLIED.md
- **API Documentation:** See API_DOCUMENTATION.md
- **Architecture:** See README.md and IMPLEMENTATION_SUMMARY.md

---

**READY FOR DEMO! 🚀**
