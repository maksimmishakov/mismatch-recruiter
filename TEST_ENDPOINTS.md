# MisMatch Recruiter - 4 Feature API Tests

## PART 1: Job Profiles Feature

### Create Job Profile
```bash
curl -X POST http://localhost:5000/api/job-profiles/ \
  -H 'Content-Type: application/json' \
  -d '{
    "job_title": "Senior Recruiter",
    "required_skills": ["Python", "Flask", "SQL"],
    "salary_range": "100k-150k",
    "description": "Senior recruiter for tech roles"
  }'
```

### Get Job Profile
```bash
curl -X GET http://localhost:5000/api/job-profiles/1
```

---

## PART 2: Salary Intelligence Feature

### Create Salary Data
```bash
curl -X POST http://localhost:5000/api/salary/ \
  -H 'Content-Type: application/json' \
  -d '{
    "position": "Senior Developer",
    "base_salary": 120000,
    "bonus_percentage": 15,
    "benefits": ["health", "401k", "remote"],
    "market_rate": 135000
  }'
```

### Optimize Salary Offer
```bash
curl -X POST http://localhost:5000/api/salary/optimize-offer \
  -H 'Content-Type: application/json' \
  -d '{
    "base_salary": 120000,
    "market_rate": 135000
  }'
```

Expected Response:
```json
{
  "base_salary": 120000,
  "market_rate": 135000,
  "optimal_salary": 127500
}
```

---

## PART 3: Lamoda Hiring DNA Feature

### Create Hiring DNA Profile
```bash
curl -X POST http://localhost:5000/api/hiring-dna/ \
  -H 'Content-Type: application/json' \
  -d '{
    "candidate_id": "cand_12345",
    "dna_profile": {"personality": "analytical", "leadership": "high"},
    "cultural_fit": 0.85,
    "technical_match": 0.92
  }'
```

### Get Hiring DNA
```bash
curl -X GET http://localhost:5000/api/hiring-dna/cand_12345
```

---

## PART 4: Real-time Signals Feature

### Create Hiring Signal
```bash
curl -X POST http://localhost:5000/api/signals/ \
  -H 'Content-Type: application/json' \
  -d '{
    "signal_type": "candidate_profile_viewed",
    "signal_value": 1.0,
    "related_entity": "cand_12345"
  }'
```

### Get Signals by Type
```bash
curl -X GET http://localhost:5000/api/signals/candidate_profile_viewed
```

---

## Implementation Status

### ✅ Completed:
- JobProfile model with fields: id, job_title, required_skills, salary_range, description, created_at
- SalaryData model with fields: id, position, base_salary, bonus_percentage, benefits, market_rate, created_at
- HiringDNA model with fields: id, candidate_id, dna_profile, cultural_fit, technical_match, created_at
- HiringSignal model with fields: id, signal_type, signal_value, related_entity, timestamp

### ✅ Routes Created:
- app/routes/job_profiles.py: POST/GET /api/job-profiles/
- app/routes/salary.py: POST /api/salary/, POST /api/salary/optimize-offer
- app/routes/hiring_dna.py: POST/GET /api/hiring-dna/
- app/routes/signals.py: POST/GET /api/signals/

### ✅ Files Modified:
- app/models.py: Added 4 new SQLAlchemy models
- app/routes.py: Added blueprint imports and registrations

### ✅ Git Commit:
- Commit: feat: add 4 recruiter intelligence features
- Branch: feature/job-enrichment-ml-matching
- Files: 6 changed, 191 insertions
