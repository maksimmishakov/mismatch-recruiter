# MISMATCH-RECRUITER: Quick Start Guide

## 📋 Project Overview

**Mismatch Recruiter** - это платформа для умного подбора кандидатов с использованием ML

- **Status:** Week 1 Production Hardening ✅ COMPLETE
- **Current Phase:** Ready for CI/CD Pipeline (Week 2)
- **Team:** Solo Developer
- **Timeline:** January 7 - January 20, 2026 (14 days)

---

## 🚀 Quick Start

### 1. Clone & Setup

```bash
git clone https://github.com/maksimmishakov/mismatch-recruiter.git
cd mismatch-recruiter/backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
cp .env.example .env
```

### 2. Configure Database

```bash
# Update .env with database credentials
nano .env

# Initialize database
python init_db.py
```

### 3. Run Backend

```bash
python app.py
# API runs on http://localhost:5000
```

### 4. Setup Frontend (in separate terminal)

```bash
cd ../frontend
npm install
echo "VITE_APP_API_URL=http://localhost:5000/api" > .env.local
npm run dev
# Frontend runs on http://localhost:5173
```

---

## ✅ Week 1: Security & Environment - COMPLETED

### 📁 Deliverables
- ✅ PostgreSQL Database Setup
- ✅ Flask Backend with SQLAlchemy ORM
- ✅ RESTful API Endpoints (CRUD)
- ✅ Input Validation with Marshmallow
- ✅ CORS Security with Whitelist
- ✅ Rate Limiting
- ✅ Sentry Error Tracking
- ✅ Comprehensive Logging
- ✅ Database Indexes & Pagination
- ✅ Security Checklist
- ✅ Deployment Guide

### 🔗 Related Files
- `SECURITY_CHECKLIST.md` - Security audit checklist
- `DEPLOYMENT_GUIDE.md` - Step-by-step deployment instructions
- `TASKS.md` - Complete 4-week project plan

---

## 📅 Week 2: CI/CD Pipeline & Deployment (Next)

### 🎯 Goals
- Setup GitHub Actions for automated testing
- Create Docker configuration for containerization
- Deploy to Amvera Cloud
- Setup monitoring and alerting

### 📝 Tasks
1. Create `.github/workflows/ci.yml` with automated tests
2. Create Dockerfile for backend and frontend
3. Setup Amvera Cloud deployment
4. Configure health checks and monitoring

### ⏱️ Timeline
- Day 5 (Jan 11): CI/CD Setup
- Day 6 (Jan 12): Amvera Deployment
- Day 7 (Jan 13): Final Testing & Launch

---

## 🏗️ Project Structure

```
mismatch-recruiter/
├── backend/
│   ├── app/
│   │   ├── models.py           # SQLAlchemy models
│   │   ├── schemas.py          # Marshmallow validation
│   │   ├── routes/             # API endpoints
│   │   ├── services/           # Business logic
│   │   ├── config.py           # Configuration
│   │   ├── database.py         # Database setup
│   │   ├── logger.py           # Logging setup
│   │   ├── errors.py           # Error handling
│   │   └── monitoring.py       # Prometheus metrics
│   ├── migrations/             # Database migrations
│   ├── tests/                  # Unit & integration tests
│   ├── requirements.txt        # Python dependencies
│   ├── docker-compose.yml      # Docker services
│   ├── DEPLOYMENT_GUIDE.md     # Deployment instructions
│   ├── SECURITY_CHECKLIST.md   # Security verification
│   └── TASKS.md                # Project task list
├── frontend/
│   ├── src/
│   │   ├── components/         # Vue components
│   │   ├── pages/              # Route pages
│   │   ├── services/           # API services
│   │   └── stores/             # State management
│   └── package.json
└── .github/
    └── workflows/              # CI/CD workflows
```

---

## 🔐 Security Features

✅ **Environment Variables** - All secrets from .env
✅ **CORS Security** - Whitelist configured
✅ **Rate Limiting** - API rate limiting enabled
✅ **Input Validation** - Marshmallow schemas
✅ **Error Handling** - GDPR-compliant error messages
✅ **Logging** - Structured logging with timestamps
✅ **Error Tracking** - Sentry integration
✅ **Database Security** - Password hashing with salt
✅ **SQL Injection Protection** - SQLAlchemy ORM
✅ **Performance** - Database indexes, pagination

---

## 🧪 Testing

### Run Tests
```bash
cd backend
pytest                 # Run all tests
pytest -v             # Verbose output
pytest --cov=app     # With coverage report
```

### Test Coverage Goals
- Models: 100%
- Routes: 80%+
- Services: 85%+
- Overall: 80%+

---

## 🚢 Deployment

### Local Development
```bash
# Terminal 1: Backend
cd backend
python app.py

# Terminal 2: Frontend
cd frontend
npm run dev
```

### Docker
```bash
cd backend
docker-compose up -d
```

### Production (Amvera Cloud)
```bash
# Automatic deployment on git push
git push origin main
# Amvera automatically builds and deploys
```

---

## 📊 Monitoring

### Health Check
```bash
curl http://localhost:5000/health
```

### Metrics
```bash
curl http://localhost:5000/metrics
```

### Logs
```bash
# Backend logs
tail -f backend/backend.log

# Docker logs
docker-compose logs -f
```

---

## 🐛 Troubleshooting

### Database Connection Error
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Check connection string in .env
echo $DATABASE_URL
```

### API Not Responding
```bash
# Check Flask app status
lsof -i :5000

# Restart backend
python app.py
```

### Frontend API Errors
```bash
# Check CORS configuration
curl -H "Origin: http://localhost:3173" http://localhost:5000/health

# Check API_URL in .env.local
cat frontend/.env.local
```

---

## 📚 Documentation

- `DEPLOYMENT_GUIDE.md` - Complete deployment guide
- `SECURITY_CHECKLIST.md` - Security verification checklist
- `TASKS.md` - Detailed 4-week project plan
- `README.md` - Project overview

---

## 🎯 Next Steps

1. **Week 2 (Jan 11-13)**: CI/CD Pipeline & Deployment
   - Setup GitHub Actions
   - Create Docker configuration
   - Deploy to Amvera Cloud

2. **Week 3 (Jan 14-16)**: Advanced Features
   - ML matching algorithm
   - Resume parsing
   - Job enrichment
   - Frontend dashboard

3. **Week 4 (Jan 17-20)**: Testing & Optimization
   - Unit tests (80%+ coverage)
   - Integration tests
   - Performance testing & optimization
   - Final review & v1.0.0 release

---

## 📞 Support

- **Issues:** GitHub Issues
- **Discussion:** GitHub Discussions
- **Monitoring:** Sentry Dashboard
- **Logs:** Backend logs in `backend/backend.log`

---

## 📝 License

Provisional License - All rights reserved (2026)
