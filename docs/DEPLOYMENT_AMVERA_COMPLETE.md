# Complete Deployment Guide: MisMatch Recruiter on Amvera Cloud

## Project Status: All Phases Complete

- ✅ Phase 2: AI Matching ML Engine (Complete)
- ✅ Phase 3: React Frontend (Complete)
- ✅ Phase 4: Advanced Features - Email, Scheduling, Analytics, Celery (Complete)
- ✅ API Testing Documentation with curl & Postman (Complete)
- 🚀 Phase 5: Deployment to Amvera Cloud (This Guide)

## Prerequisites

1. **Amvera Cloud Account** - https://cloud.amvera.ru
2. **GitHub Account** - Repository access
3. **Docker** - For local testing (optional but recommended)
4. **Amvera CLI** - For advanced management

## Architecture Overview

```
┌─────────────────────────────────────────────┐
│       Amvera Cloud Container                │
│  ┌──────────────────────────────────────┐   │
│  │  Flask Application (Python)          │   │
│  │  - ML Matching Engine                │   │
│  │  - REST API Endpoints                │   │
│  │  - React Frontend (SPA)              │   │
│  └──────────────────────────────────────┘   │
│  ┌──────────────────────────────────────┐   │
│  │  PostgreSQL Database                 │   │
│  │  - Candidates, Jobs, Matches         │   │
│  └──────────────────────────────────────┘   │
│  ┌──────────────────────────────────────┐   │
│  │  Redis Cache & Celery Tasks          │   │
│  │  - Email notifications               │   │
│  │  - Async job processing              │   │
│  └──────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

## Step 1: Prepare Application for Deployment

### 1.1 Create Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Install Node.js for frontend build
RUN apt-get update && apt-get install -y nodejs npm && rm -rf /var/lib/apt/lists/*

# Build React frontend
WORKDIR /app/static
RUN npm install
RUN npm run build

WORKDIR /app

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "app:create_app()"]
```

### 1.2 Update requirements.txt

Ensure all production dependencies are listed:

```
Flask==2.3.0
Flask-SQLAlchemy==3.0.0
Flask-Migrate==4.0.0
Flask-Mail==0.9.1
SQLAlchemy==2.0.0
psycopg2-binary==2.9.6
celery==5.3.0
redis==4.5.0
gunicorn==20.1.0
python-dotenv==1.0.0
requests==2.31.0
numpy==1.24.0
scikit-learn==1.2.0
jinja2==3.1.2
pytest==7.3.0
pytest-flask==1.2.0
```

### 1.3 Create .env.example

```bash
# Flask Configuration
FLASK_ENV=production
FLASK_APP=app:create_app
SECRET_KEY=your-secret-key-here
DEBUG=False

# Database
DATABASE_URL=postgresql://user:password@postgres:5432/mismatch_recruiter
DB_NAME=mismatch_recruiter
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=postgres
DB_PORT=5432

# Redis
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=noreply@mismatchrecruiter.com

# Application
APP_NAME=MisMatch Recruiter
APP_VERSION=1.0.0
LOG_LEVEL=INFO
```

## Step 2: Push to GitHub

```bash
git add .
git commit -m "chore: Prepare application for Amvera deployment"
git push origin master
```

## Step 3: Deploy on Amvera Cloud

### 3.1 Create New Project on Amvera

1. Go to https://cloud.amvera.ru
2. Sign in with your account
3. Click "New Project"
4. Select "Git Repository"
5. Choose "GitHub" as source
6. Authorize GitHub access
7. Select your repository: `maksimmishakov/mismatch-recruiter`
8. Select branch: `master`

### 3.2 Configure Application Settings

1. **Project Name:** MisMatch Recruiter
2. **Instance Type:** Standard (or higher for production)
3. **Port:** 5000
4. **Command:** `gunicorn --bind 0.0.0.0:5000 --workers 4 app:create_app()`

### 3.3 Configure Environment Variables

In Amvera Dashboard:

```
FLASK_ENV = production
FLASK_APP = app:create_app
SECRET_KEY = [generate-secure-key]
DATABASE_URL = [connection-string-from-amvera-postgres]
REDIS_URL = [connection-string-from-amvera-redis]
MAIL_SERVER = smtp.gmail.com
MAIL_USERNAME = [your-email@gmail.com]
MAIL_PASSWORD = [app-specific-password]
```

### 3.4 Add PostgreSQL Database

1. In Amvera Dashboard, add service: **PostgreSQL**
2. Configure:
   - Database Name: `mismatch_recruiter`
   - Username: `postgres`
   - Password: [auto-generated, save it]
3. Amvera will provide connection string automatically

### 3.5 Add Redis Cache

1. In Amvera Dashboard, add service: **Redis**
2. Use default settings
3. Amvera will provide connection URL automatically

## Step 4: Deploy Application

### 4.1 Manual Deployment

1. Go to your Amvera project dashboard
2. Click "Deploy"
3. Select "From Git"
4. Choose "master" branch
5. Click "Deploy Now"

Amvera will:
- Pull code from GitHub
- Build Docker image
- Run database migrations
- Start services
- Assign domain name

### 4.2 Monitor Deployment

```bash
# View logs
amvera logs --follow

# Check status
amvera status

# Restart application
amvera restart
```

## Step 5: Post-Deployment Configuration

### 5.1 Run Database Migrations

```bash
# SSH into container
amvera ssh

# Run migrations
flask db upgrade

# Create initial data (optional)
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"

# Exit
exit
```

### 5.2 Test API Endpoints

```bash
# Get your Amvera domain
AMVERA_DOMAIN=$(amvera info | grep "Domain:" | awk '{print $2}')

# Test health check
curl https://$AMVERA_DOMAIN/api/health

# Test calculate match
curl -X POST https://$AMVERA_DOMAIN/api/matches/calculate-score \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": 1,
    "job_id": 1
  }'

# Test get matches
curl https://$AMVERA_DOMAIN/api/matches
```

### 5.3 Access React Frontend

Open in browser:
```
https://your-amvera-domain.app/
```

You should see MisMatch Recruiter React application.

## Step 6: Configure Domain (Optional)

### 6.1 Custom Domain

1. Go to Amvera Dashboard → Project Settings
2. Click "Add Custom Domain"
3. Enter your domain (e.g., `mismatch-recruiter.com`)
4. Update DNS records to point to Amvera
5. Verify domain

### 6.2 SSL Certificate

Amvera automatically provides free SSL certificates (Let's Encrypt).

## Step 7: Monitoring & Maintenance

### 7.1 View Application Logs

```bash
amvera logs --follow --since 1h
```

### 7.2 Monitor Resources

```bash
amvera metrics
```

### 7.3 Database Backups

In Amvera Dashboard:
1. Go to PostgreSQL service
2. Configure automated backups (daily)
3. Download manual backups as needed

### 7.4 Scaling

```bash
# Scale workers
amvera scale --workers 8

# Scale instance
amvera scale --instance large
```

## Step 8: Production Best Practices

### 8.1 Security

- ✅ Use strong SECRET_KEY (minimum 32 characters)
- ✅ Enable HTTPS (automatic in Amvera)
- ✅ Use environment variables for sensitive data
- ✅ Regular security updates
- ✅ Enable database encryption

### 8.2 Performance

- ✅ Enable Redis caching
- ✅ Use Celery for async tasks
- ✅ Optimize database queries
- ✅ Enable GZIP compression
- ✅ CDN for static files

### 8.3 Monitoring

- ✅ Application error tracking (Sentry)
- ✅ Performance monitoring (New Relic)
- ✅ Log aggregation (ELK Stack)
- ✅ Uptime monitoring
- ✅ Email alerts

## Troubleshooting

### Issue: Database Connection Failed
```bash
# Check database URL
amvera env | grep DATABASE_URL

# Test connection
psql $DATABASE_URL -c "SELECT version();"
```

### Issue: Memory Limit Exceeded
```bash
# Increase instance size
amvera scale --instance xlarge

# Optimize application
# - Reduce worker count if needed
# - Enable caching
```

### Issue: Slow API Responses
```bash
# Check logs
amvera logs --follow

# Monitor metrics
amvera metrics

# Scale workers
amvera scale --workers 8
```

## Deployment Summary

| Component | Service | Status |
|-----------|---------|--------|
| Flask Backend | Python 3.9 | ✅ Running |
| React Frontend | Node.js SPA | ✅ Running |
| Database | PostgreSQL | ✅ Running |
| Cache | Redis | ✅ Running |
| Email Queue | Celery | ✅ Running |
| API Endpoints | REST | ✅ Operational |
| SSL Certificate | Let's Encrypt | ✅ Active |

## Success Indicators

✅ All phases implemented (Phase 2-4)
✅ API endpoints tested with curl/Postman
✅ React frontend deployed and accessible
✅ Database running and migrations complete
✅ Email notifications queued via Celery
✅ Application running on Amvera Cloud
✅ Custom domain configured (optional)
✅ Monitoring and logging enabled

## Next Steps

1. **Monitor** - Watch deployment logs and metrics
2. **Test** - Run comprehensive API tests
3. **Optimize** - Fine-tune performance settings
4. **Scale** - Increase resources as needed
5. **Maintain** - Regular updates and security patches

## Support Resources

- [Amvera Documentation](https://docs.amvera.ru/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://react.dev/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Redis Documentation](https://redis.io/documentation)
- [Celery Documentation](https://docs.celeryproject.io/)

## Contact & Support

For issues or questions:
- GitHub Issues: https://github.com/maksimmishakov/mismatch-recruiter/issues
- Email: maksim@example.com
- Amvera Support: https://cloud.amvera.ru/support
