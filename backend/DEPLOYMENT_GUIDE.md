# Deployment Guide

## Prerequisites

- Python 3.12+
- PostgreSQL 15+
- Node.js 24+
- Docker & Docker Compose (optional)
- Git

## Environment Setup

### 1. Clone Repository
```bash
git clone https://github.com/maksimmishakov/mismatch-recruiter.git
cd mismatch-recruiter
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\\Scripts\\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your values
nano .env

# Initialize database
python init_db.py

# Run migrations (if applicable)
flask db upgrade

# Start server
python app.py
# Runs on http://localhost:5000
```

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Setup environment variables
echo "VITE_APP_API_URL=http://localhost:5000/api" > .env.local

# Start development server
npm run dev
# Runs on http://localhost:5173
```

## Production Deployment

### 1. Database Setup
```bash
# Create PostgreSQL database
psql postgres

CREATE USER mismatch WITH PASSWORD 'your-secure-password';
CREATE DATABASE mismatch OWNER mismatch;
ALTER USER mismatch CREATEDB;
```

### 2. Environment Variables
```bash
# Create .env.production
cat > backend/.env.production << 'ENV_EOF'
FLASK_ENV=production
FLASK_DEBUG=False
DATABASE_URL=postgresql://mismatch:password@localhost:5432/mismatch
JWT_SECRET_KEY=your-256-bit-secret-key
CORS_ORIGINS=https://yourdomain.com
LOG_LEVEL=INFO
SENTRY_DSN=your-sentry-dsn
ENV_EOF
```

### 3. Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose -f docker-compose.yml up -d

# Check status
docker-compose logs -f

# Stop services
docker-compose down
```

### 4. Amvera Cloud Deployment
```bash
# Login to Amvera
amvera login

# Create app
amvera app:create mismatch-recruiter

# Deploy
git push amvera main
```

### 5. SSL/TLS Setup
```bash
# Using Let's Encrypt with Nginx
sudo certbot certonly --webroot -w /var/www/html -d yourdomain.com

# Configure nginx with SSL
# See nginx.conf example
```

## Post-Deployment

### Health Checks
```bash
# Check API
curl https://api.yourdomain.com/health

# Check database
curl https://api.yourdomain.com/api/candidates
```

### Monitoring
- Sentry: https://sentry.io/projects/
- Logs: /var/log/mismatch/
- Metrics: /metrics endpoint (if Prometheus enabled)

### Backup & Recovery
```bash
# Backup database
pg_dump mismatch > backup-$(date +%Y%m%d).sql

# Restore from backup
psql mismatch < backup-20260104.sql
```

## Troubleshooting

### Database Connection Error
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check connection string in .env
# Format: postgresql://user:password@host:port/database
```

### API Not Responding
```bash
# Check logs
docker-compose logs backend

# Restart service
docker-compose restart backend
```

### High Memory Usage
```bash
# Check running processes
docker stats

# Scale backend instances
docker-compose up -d --scale backend=3
```

## Security

- Always use HTTPS in production
- Rotate JWT_SECRET_KEY regularly
- Keep dependencies updated
- Monitor Sentry for errors
- Review logs regularly
- Use strong PostgreSQL passwords
