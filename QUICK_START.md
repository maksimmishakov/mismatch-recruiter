# MisMatch Recruiter - Quick Start Guide

## 🚀 Get Up and Running in 5 Minutes

### Prerequisites
- Docker and Docker Compose installed
- Git installed
- Terminal/Command prompt access

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/mismatch-recruiter.git
cd mismatch-recruiter
```

### Step 2: Create Environment File

```bash
cp .env.example .env
```

The default .env file is configured for local development.

### Step 3: Build and Start Services

```bash
docker-compose up --build
```

This will:
- Build the backend and frontend Docker images
- Start PostgreSQL database
- Start Flask backend on http://localhost:5000
- Start React frontend on http://localhost:3000

### Step 4: Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000/api
- **API Documentation**: See API_DOCUMENTATION.md

## Testing the API

### Health Check

```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{"status": "healthy", "service": "mismatch-recruiter-api"}
```

### Register a User

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "testuser",
    "password": "password123",
    "full_name": "Test User"
  }'
```

### Login

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

## Running Tests

### Backend Tests

```bash
docker-compose exec backend pytest
```

With coverage:
```bash
docker-compose exec backend pytest --cov=app
```

### Linting

```bash
docker-compose exec backend flake8 app
```

## Useful Docker Commands

### View Logs

```bash
# Backend logs
docker-compose logs -f backend

# Frontend logs
docker-compose logs -f frontend

# Database logs
docker-compose logs -f db
```

### Stop Services

```bash
docker-compose down
```

### Rebuild Images

```bash
docker-compose build --no-cache
```

### Access Database

```bash
docker-compose exec db psql -U recruiter_user -d mismatch_recruiter
```

## File Structure Quick Reference

```
├── backend/           # Flask application
├── frontend/          # React application
├── docker-compose.yml # Service orchestration
├── .env.example       # Environment template
├── README.md          # Full documentation
├── API_DOCUMENTATION.md
├── DEPLOYMENT_GUIDE.md
└── IMPLEMENTATION_SUMMARY.md
```

## Next Steps

1. **Read the full README.md** for comprehensive documentation
2. **Check API_DOCUMENTATION.md** for all API endpoints
3. **Review DEPLOYMENT_GUIDE.md** for production deployment
4. **Explore the code** - Start with `backend/app/__init__.py` and `frontend/src/App.js`

## Troubleshooting

### Port Already in Use

If port 5000, 3000, or 5432 is already in use:

```bash
# Find and kill the process
sudo lsof -i :5000
sudo kill -9 <PID>
```

### Database Connection Error

```bash
# Check if database container is running
docker-compose ps db

# Restart the database
docker-compose restart db
```

### Out of Memory

```bash
# Clean up Docker system
docker system prune -a
```

## Support

For issues or questions:
1. Check the documentation files
2. Review GitHub issues
3. Contact the development team

Happy coding! 🎉
