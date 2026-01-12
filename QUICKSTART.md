# LAMODA Recruiter - Quick Start Guide

## 🚀 Quick Start (5 minutes)

### Prerequisites
- Python 3.12+
- Docker & Docker Compose (optional)
- curl for API testing

### Option 1: Local Development (Fastest)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the Flask API
python -m flask --app app run --host 0.0.0.0 --port 5000

# 3. In another terminal, run the demo
./DEMO_SCRIPT.sh
```

### Option 2: Docker

```bash
# 1. Build and start services
docker-compose up -d

# 2. Wait for services to be healthy
sleep 10

# 3. Run demo
./DEMO_SCRIPT.sh
```

## 📊 API Endpoints

### Health Check
```bash
curl http://localhost:5000/api/health
```

### Candidates
```bash
# List candidates
curl http://localhost:5000/api/candidates

# Create candidate
curl -X POST http://localhost:5000/api/candidates \
  -H 'Content-Type: application/json' \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "skills": ["Python", "Flask"],
    "experience_years": 5
  }'
```

### Jobs
```bash
# List jobs
curl http://localhost:5000/api/jobs

# Create job
curl -X POST http://localhost:5000/api/jobs \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "Python Developer",
    "description": "Looking for Python developer",
    "company": "LAMODA",
    "location": "Moscow",
    "salary_min": 100000,
    "salary_max": 200000,
    "required_skills": ["Python", "Flask"]
  }'
```

### Matches
```bash
# List matches
curl http://localhost:5000/api/matches

# Create match
curl -X POST http://localhost:5000/api/matches \
  -H 'Content-Type: application/json' \
  -d '{
    "candidate_id": 1,
    "job_id": 1,
    "match_score": 85.5,
    "status": "pending"
  }'
```

## 📁 Project Structure

```
mismatch-recruiter/
├── app/
│   ├── __init__.py          # Flask application factory
│   ├── models/              # Database models
│   │   ├── user.py
│   │   ├── candidate.py
│   │   ├── job.py
│   │   └── match.py
│   └── routes/              # API endpoints
│       └── __init__.py
├── docker-compose.yaml       # Docker configuration
├── wsgi.py                   # Gunicorn entry point
├── .env                      # Environment configuration
└── requirements.txt          # Python dependencies
```

## 🔧 Environment Variables

```bash
FLASK_ENV=development
DATABASE_URL=sqlite:///lamoda.db
SECRET_KEY=your-secret-key
JWT_SECRET=your-jwt-secret
REDIS_URL=redis://localhost:6379/0
```

## ✅ System Status

- ✅ Flask API: Running on http://localhost:5000
- ✅ Database: SQLite (local) / PostgreSQL (production)
- ✅ Redis Cache: Ready
- ✅ Docker: Ready for production deployment

## 📚 Documentation

- `PRODUCTION_READY_REPORT.md` - Detailed production report
- `FINAL_SUMMARY.txt` - Project completion summary
- `DEMO_SCRIPT.sh` - Automated demo script

## 🎯 Next Steps

1. Start the API: `python -m flask --app app run`
2. Run the demo: `./DEMO_SCRIPT.sh`
3. Check the API at: http://localhost:5000/api/health

## 📞 Support

For issues or questions, please check:
1. `PRODUCTION_READY_REPORT.md` for detailed information
2. API logs in `logs/` directory
3. Database file at `lamoda.db`

---
**Status:** 🎉 100% Production Ready for Demo  
**Last Updated:** January 12, 2026
