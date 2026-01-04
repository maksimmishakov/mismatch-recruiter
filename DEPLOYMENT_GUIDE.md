# MisMatch Recruiter Platform - Deployment Guide

## Overview
This guide provides comprehensive instructions for deploying the MisMatch Recruiter Platform, a full-stack AI-powered recruiting application built with React/TypeScript (Frontend) and Python Flask (Backend).

## Architecture
- **Frontend**: React 18 with TypeScript, Vite bundler, Redux state management, Tailwind CSS
- **Backend**: Python 3.x with Flask/FastAPI, RESTful API
- **Database**: PostgreSQL (configured for production)
- **Deployment**: Docker containers with orchestration support

## System Requirements

### Development
- Node.js 16+ (18+ recommended)
- Python 3.8+
- npm or yarn
- Git

### Production
- Docker & Docker Compose
- Linux server or cloud container platform
- Minimum 2GB RAM, 2 CPU cores
- 5GB storage

## Installation & Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd mismatch-recruiter
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev          # Development
npm run build        # Production build
npm run preview      # Preview build
```

Frontend runs on: http://localhost:3001

### 3. Backend Setup
```bash
# Install Python dependencies
pip3 install -r requirements.txt

# Run development server
python3 api_server.py
```

Backend API runs on: http://localhost:8000

## Docker Deployment

### Build Images
```bash
docker-compose build
```

### Start Services
```bash
docker-compose up -d
```

### Access Services
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Environment Configuration

Create `.env` file in root directory:
```env
# Backend
DATABASE_URL=postgresql://user:password@localhost/mismatch_db
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

# Frontend
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=MisMatch
```

## Project Structure
```
mismatch-recruiter/
├── frontend/           # React/TypeScript frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── store/     # Redux state
│   │   └── services/  # API calls
│   └── package.json
├── backend/            # Python backend (root level)
│   ├── api_server.py
│   ├── app.py
│   └── requirements.txt
├── docker-compose.yml
├── Dockerfile
└── README.md
```

## Key Features Implemented

### Frontend
✅ Responsive UI with Tailwind CSS
✅ Authentication/Login system
✅ Dashboard for recruiters
✅ Candidates management
✅ Jobs listing and management
✅ Match analytics
✅ Redux state management
✅ React Router for navigation
✅ Protected routes
✅ TypeScript support

### Backend
✅ RESTful API endpoints
✅ Authentication middleware
✅ Candidate database models
✅ Jobs API endpoints
✅ Matching algorithm
✅ OpenAPI/Swagger documentation
✅ Error handling
✅ CORS support

## Testing

### Frontend Tests
```bash
cd frontend
npm run test
npm run test:ui      # UI test runner
```

### Backend Tests
```bash
python3 -m pytest
```

## Production Deployment

### Using Docker
```bash
# Build production image
docker build -t mismatch-recruiter:latest .

# Run container
docker run -p 8000:8000 -p 3000:3000 mismatch-recruiter:latest
```

### Using Cloud Platforms

#### Heroku
```bash
heroku create mismatch-recruiter
git push heroku main
```

#### AWS/GCP/Azure
- Use container registry (ECR/GCR/ACR)
- Deploy via Kubernetes or App Engine
- Configure environment variables in cloud console

### Nginx Reverse Proxy Configuration
```nginx
upstream frontend {
    server localhost:3000;
}

upstream backend {
    server localhost:8000;
}

server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://frontend;
    }

    location /api {
        proxy_pass http://backend;
    }
}
```

## Monitoring & Logging

- Frontend: Browser DevTools, error boundaries
- Backend: Python logging module
- Containers: Docker logs `docker logs <container-id>`
- Metrics: Prometheus/Grafana integration (optional)

## Troubleshooting

### Port Already in Use
```bash
# Find process using port
lsof -i :8000
# Kill process
kill -9 <PID>
```

### Database Connection Error
- Verify PostgreSQL is running
- Check DATABASE_URL in environment
- Ensure database exists: `createdb mismatch_db`

### CORS Issues
- Update ALLOWED_ORIGINS in backend config
- Verify VITE_API_URL in frontend .env

### Build Failures
- Clear npm cache: `npm cache clean --force`
- Reinstall dependencies: `rm -rf node_modules && npm install`
- Check Node version: `node --version`

## API Documentation

Once backend is running, view API docs at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Performance Optimization

### Frontend
- Code splitting with React.lazy()
- Image optimization
- CSS minification (Vite handles automatically)
- Lazy loading components

### Backend
- Database indexing
- Query optimization
- Caching strategy
- Load balancing with Nginx

## Security Checklist

- [ ] Update all dependencies regularly
- [ ] Set secure SECRET_KEY in production
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Use environment variables for secrets
- [ ] Implement rate limiting
- [ ] Enable CSRF protection
- [ ] Regular security audits
- [ ] Database backups configured
- [ ] API authentication tokens configured

## Maintenance

### Regular Updates
```bash
# Frontend
cd frontend
npm update
npm audit fix

# Backend
pip install --upgrade pip
pip install -r requirements.txt --upgrade
```

### Backup Strategy
- Daily database backups
- Code repository backups (Git)
- Configuration backups
- Document retention policy

## Support & Troubleshooting

For issues or questions:
1. Check error logs
2. Review API documentation
3. Check GitHub issues
4. Contact development team

## Version History

- v1.0.0 (2024-01): Initial release
  - Frontend React setup
  - Backend API foundation  
  - Docker support
  - Authentication system
  - Core recruiting features

## License

This project is licensed under MIT License.

