# Deployment & DevOps Guide - MisMatch Recruiter

## Overview
Comprehensive guide for deploying MisMatch Recruiter using multiple strategies (Docker, Kubernetes, Amvera).

## Prerequisites
- Docker & Docker Compose
- Node.js 18+
- PostgreSQL 15+
- Git
- GitHub secrets configured

## Local Deployment

### Using Docker Compose
```bash
docker-compose up -d
# Frontend: http://localhost:3000
# API: http://localhost:5000
# PostgreSQL: localhost:5432
# Redis: localhost:6379
```

### Using Docker
```bash
docker build -t mismatch-recruiter:latest .
docker run -p 3000:3000 mismatch-recruiter:latest
```

## Production Deployment

### GitHub Actions CI/CD
Automatically runs on push to main:
1. **Test**: Run Vitest suite with coverage
2. **Lint**: ESLint and code quality checks
3. **Security**: npm audit for vulnerabilities
4. **Deploy**: Push to Amvera on success

### Deploy to Amvera
1. Set `AMVERA_TOKEN` in GitHub Secrets
2. Push to main branch
3. GitHub Actions triggers deployment
4. Access at: https://mismatch-recruiter-maksimisakov.amvera.io

## Environment Variables

### Frontend (.env.production)
```
VITE_API_URL=https://api.mismatch.io
VITE_GOOGLE_ANALYTICS_ID=UA-XXXXXXXXX-1
VITE_SENTRY_DSN=https://...@sentry.io/...
```

### Backend
```
DATABASE_URL=postgresql://user:password@db:5432/mismatch
REDIS_URL=redis://localhost:6379
JWT_SECRET=your-secret-key
AMVERA_TOKEN=your-amvera-token
```

## Performance Metrics

### Target Metrics
- Time to Interactive (TTI): < 2s
- First Contentful Paint (FCP): < 1s
- Largest Contentful Paint (LCP): < 2.5s
- Cumulative Layout Shift (CLS): < 0.1
- Lighthouse Score: 90+

### Monitoring
- New Relic / Sentry for error tracking
- PageSpeed Insights for performance
- Uptime monitoring via Amvera

## Rollback Procedure
```bash
# Get previous deployment hash
git log --oneline

# Rollback to previous version
git reset --hard <commit-hash>
git push origin main --force-with-lease

# CI/CD will trigger redeploy
```

## Security Checklist
- [ ] HTTPS enabled
- [ ] Environment variables secured
- [ ] Dependencies up to date
- [ ] Security headers configured
- [ ] CORS properly configured
- [ ] Rate limiting enabled
- [ ] Input validation implemented
- [ ] XSS prevention active
- [ ] CSRF tokens used
- [ ] Authentication tokens secured

