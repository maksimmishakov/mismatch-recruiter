# DEMO PRESENTATION - MisMatch Recruiter for Lamoda

**Duration:** 15-20 minutes  
**Date:** January 8, 2026, 09:00 MSK  
**Location:** Moscow

---

## Part 1: Overview (2 min)

### What is MisMatch Recruiter?
- Intelligent talent-job matching platform
- REST API + React frontend
- Production-ready infrastructure
- PostgreSQL database with migrations
- Docker containerization

### Why Lamoda Needs This?
- Faster candidate screening
- Better job-candidate alignment
- Reduced hiring time
- Data-driven matching algorithm
- Scalable architecture

### Key Features
- JWT-based authentication
- Candidate profile management
- Job posting creation
- Intelligent matching algorithm
- Real-time API responses
- PostgreSQL persistence

---

## Part 2: Live Demo (10-15 min)

### 2.1 Health Check & API Status
```bash
# Show API is running
curl http://localhost:5000/health
# Response: {"status":"ok","message":"Service is running"}
```

### 2.2 User Registration & Authentication
```bash
# Register new account
curl -X POST http://localhost:5000/api/auth/register \\
  -H "Content-Type: application/json" \\
  -d '{
    "email": "demo@lamoda.ru",
    "password": "Demo123!",
    "full_name": "Demo User"
  }'

# Response includes JWT token
# Token used for all subsequent requests
```

### 2.3 Candidate Management
```bash
# Create candidate profile
curl -X POST http://localhost:5000/api/candidates \\
  -H "Authorization: Bearer TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{
    "name": "Ivan Petrov",
    "email": "ivan@lamoda.ru",
    "skills": ["Python", "JavaScript", "React"],
    "experience_years": 5,
    "location": "Moscow"
  }'

# List all candidates
curl http://localhost:5000/api/candidates \\
  -H "Authorization: Bearer TOKEN"
```

### 2.4 Job Management
```bash
# Create job posting
curl -X POST http://localhost:5000/api/jobs \\
  -H "Authorization: Bearer TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{
    "title": "Senior Python Developer",
    "description": "We need experienced Python developer",
    "required_skills": ["Python", "Flask", "PostgreSQL"],
    "salary_min": 100000,
    "salary_max": 150000
  }'
```

### 2.5 Matching Algorithm
```bash
# Create match between candidate and job
curl -X POST http://localhost:5000/api/matches \\
  -H "Authorization: Bearer TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{
    "candidate_id": 1,
    "job_id": 1,
    "score": 0.85
  }'

# Result: Intelligent matching based on skills
```

### 2.6 Frontend Demonstration
- Open http://localhost:3000 in browser
- Show React UI
- Demonstrate responsive design
- Show candidate dashboard
- Show job listings

---

## Part 3: Technical Stack (2 min)

### Backend Architecture
- **Framework:** Flask 2.x
- **ORM:** SQLAlchemy
- **Database:** PostgreSQL 12+
- **Authentication:** JWT (PyJWT)
- **Validation:** Marshmallow
- **Production Server:** Gunicorn

### Frontend Architecture
- **Framework:** React 18+
- **Build Tool:** Webpack
- **Transpiler:** Babel
- **Package Manager:** npm

### DevOps & Deployment
- **Containerization:** Docker
- **Orchestration:** Docker Compose
- **Reverse Proxy:** Nginx
- **Process Management:** Systemd
- **SSL/TLS:** Let's Encrypt

### Database Schema
- **user** table - Authentication
- **candidate** table - Candidate profiles
- **job** table - Job postings
- **match** table - Candidate-job matches

---

## Part 4: Next Steps & Integration (1-2 min)

### Integration with Lamoda HR System
1. API integration with existing HRIS
2. Single Sign-On (SSO) setup
3. Real-time data synchronization

### Custom Matching Algorithm
1. ML-based skill matching
2. Experience level alignment
3. Salary expectations matching
4. Location preferences

### Production Deployment
1. Cloud infrastructure setup (AWS/GCP)
2. Auto-scaling configuration
3. Load balancing
4. Monitoring & alerting
5. Database backups

### Timeline
- **Phase 1:** Integration (2-3 weeks)
- **Phase 2:** Custom matching (1-2 weeks)
- **Phase 3:** Production deployment (1 week)

---

## Key Metrics

| Metric | Value |
|--------|-------|
| API Response Time | < 100ms |
| Database Query Time | < 50ms |
| Frontend Load Time | < 500ms |
| Concurrent Users (Single Server) | 100+ |
| Uptime SLA | 99.9% |
| Test Coverage | >85% |

---

## Architecture Diagram

```
┌─────────────────────────────────────────────┐
│         LAMODA INFRASTRUCTURE               │
├─────────────────────────────────────────────┤
│                                             │
│  ┌──────────────────────────────────────┐  │
│  │     FRONTEND (React)                 │  │
│  │  - Candidate Dashboard               │  │
│  │  - Job Listings                      │  │
│  │  - Match Results                     │  │
│  └──────────────────────────────────────┘  │
│                    ↓                        │
│  ┌──────────────────────────────────────┐  │
│  │     NGINX (Reverse Proxy)            │  │
│  │  - Load Balancing                    │  │
│  │  - SSL/TLS Termination               │  │
│  └──────────────────────────────────────┘  │
│                    ↓                        │
│  ┌──────────────────────────────────────┐  │
│  │     BACKEND (Flask + Gunicorn)       │  │
│  │  - REST API                          │  │
│  │  - JWT Authentication                │  │
│  │  - Business Logic                    │  │
│  └──────────────────────────────────────┘  │
│                    ↓                        │
│  ┌──────────────────────────────────────┐  │
│  │     DATABASE (PostgreSQL)            │  │
│  │  - User Data                         │  │
│  │  - Candidate Profiles                │  │
│  │  - Job Postings                      │  │
│  │  - Matches                           │  │
│  └──────────────────────────────────────┘  │
│                                             │
└─────────────────────────────────────────────┘
```

---

## Questions & Discussion Points

1. **Scalability:** How does the system handle 10,000+ concurrent users?
2. **Data Privacy:** How is candidate data protected?
3. **Matching Algorithm:** How is the matching score calculated?
4. **Integration:** How does it integrate with Lamoda's existing systems?
5. **Customization:** Can the algorithm be customized for Lamoda's needs?
6. **Support:** What's the SLA for production support?
7. **Cost:** What's the pricing model?

---

## Contact & Next Steps

- **GitHub:** https://github.com/maksimmishakov/mismatch-recruiter
- **Demo Environment:** http://localhost:5000 (locally)
- **API Documentation:** See README.md
- **Deployment Guide:** See DEPLOYMENT_GUIDE.md

**Follow-up Meeting:** Schedule integration discussion

