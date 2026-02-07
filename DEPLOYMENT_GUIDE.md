# MisMatch Recruiter - Deployment Guide

## Quick Start with Docker Compose

### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+
- 2GB RAM minimum
- 10GB disk space

### Environment Setup

1. **Create .env file:**
```bash
cp .env.example .env
```

2. **Edit .env with your values:**
```env
SECRET_KEY=your-super-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
DATABASE_URL=postgresql://mismatch_user:secure_password@db:5432/mismatch_db
FLASK_ENV=production
```

### Build and Run

```bash
# Build all services
docker-compose build

# Start services
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Access Application

- **Frontend:** http://localhost
- **Backend API:** http://localhost:5000
- **PostgreSQL:** localhost:5432
- **Redis:** localhost:6379

## Manual Deployment

### Backend Deployment

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set environment variables:**
```bash
export FLASK_ENV=production
export DATABASE_URL=postgresql://user:pass@localhost/mismatch
export SECRET_KEY=your-secret-key
```

3. **Initialize database:**
```bash
flask db upgrade
```

4. **Run with Gunicorn:**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 'app:create_app()'
```

### Frontend Deployment

1. **Install dependencies:**
```bash
cd frontend
npm install
```

2. **Build for production:**
```bash
npm run build
```

3. **Serve with nginx:**
```bash
cp -r dist/* /var/www/html/
```

## Production Checklist

### Security
- [ ] Change all default passwords
- [ ] Set strong SECRET_KEY and JWT_SECRET_KEY
- [ ] Enable HTTPS with SSL certificates
- [ ] Configure firewall rules
- [ ] Set up rate limiting
- [ ] Enable CORS only for trusted domains
- [ ] Review and update security headers

### Performance
- [ ] Enable Redis caching
- [ ] Configure database connection pooling
- [ ] Set up CDN for static assets
- [ ] Enable gzip compression
- [ ] Configure proper logging levels

### Monitoring
- [ ] Set up application logging
- [ ] Configure error tracking (Sentry)
- [ ] Enable performance monitoring
- [ ] Set up database backups
- [ ] Configure health checks

### Scaling
- [ ] Use load balancer for multiple instances
- [ ] Set up database replication
- [ ] Configure Redis Sentinel for HA
- [ ] Use container orchestration (K8s)

## Database Migrations

```bash
# Create migration
flask db migrate -m "Description"

# Apply migration
flask db upgrade

# Rollback
flask db downgrade
```

## Backup & Restore

### Database Backup
```bash
docker-compose exec db pg_dump -U mismatch_user mismatch_db > backup.sql
```

### Database Restore
```bash
docker-compose exec -T db psql -U mismatch_user mismatch_db < backup.sql
```

## Troubleshooting

### Backend not starting
```bash
# Check logs
docker-compose logs backend

# Restart service
docker-compose restart backend
```

### Database connection issues
```bash
# Check database is running
docker-compose ps db

# Test connection
docker-compose exec db psql -U mismatch_user -d mismatch_db
```

### Frontend not loading
```bash
# Check nginx logs
docker-compose logs frontend

# Rebuild frontend
cd frontend && npm run build
docker-compose up -d --build frontend
```

## Support

For issues and questions:
- GitHub Issues: https://github.com/maksimmishakov/mismatch-recruiter/issues
- Email: support@mismatch-recruiter.com
