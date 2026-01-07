# MisMatch Recruiter - Production-Ready Talent Matching Platform

[![GitHub Actions](https://github.com/maksimmishakov/mismatch-recruiter/workflows/CI/CD/badge.svg)](https://github.com/maksimmishakov/mismatch-recruiter/actions)
[![Code Quality](https://img.shields.io/badge/code_quality-A-brightgreen)](https://github.com/maksimmishakov/mismatch-recruiter)
[![Test Coverage](https://img.shields.io/badge/coverage-85%25-brightgreen)](https://github.com/maksimmishakov/mismatch-recruiter)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Overview

MisMatch Recruiter is a sophisticated, production-ready talent matching platform that uses advanced algorithms to match job candidates with job opportunities. Built with Flask, PostgreSQL, and modern DevOps practices, the platform demonstrates enterprise-grade software engineering practices.

## Key Features

- **Intelligent Matching Algorithm**: Advanced candidate-to-job matching with skill analysis
- **RESTful API**: Comprehensive API endpoints for all operations
- **Real-time Notifications**: WebSocket support for instant updates
- **PostgreSQL Database**: Robust relational database with migrations
- **Redis Caching**: Fast data retrieval and session management
- **Docker Deployment**: Container-based deployment for consistency
- **Comprehensive Testing**: Unit and integration tests with >85% coverage
- **CI/CD Pipeline**: GitHub Actions automated testing and deployment
- **Security**: CSRF protection, secure password handling, rate limiting

## Architecture

### Tech Stack

**Backend:**
- Flask 2.x - Web framework
- SQLAlchemy - ORM
- PostgreSQL - Relational database
- Redis - Caching and session store
- Gunicorn - Production WSGI server

**Frontend:**
- React - UI framework
- Webpack - Module bundler
- Babel - JavaScript transpiler

**DevOps:**
- Docker & Docker Compose
- GitHub Actions
- Nginx - Reverse proxy
- Systemd - Process management

## Project Structure

```
mismatch-recruiter/
├── backend/                    # Flask application
│   ├── app/                   # Application package
│   │   ├── blueprints/        # Route blueprints
│   │   ├── models/            # Database models
│   │   ├── services/          # Business logic
│   │   ├── utils/             # Utility functions
│   │   ├── migrations/        # Database migrations
│   │   └── __init__.py        # App factory
│   ├── tests/                 # Test suite
│   │   ├── test_models.py     # Model tests
│   │   ├── test_api.py        # API tests
│   │   └── conftest.py        # Pytest configuration
│   ├── requirements.txt        # Python dependencies
│   ├── Dockerfile             # Container definition
│   └── wsgi.py                # WSGI entry point
├── frontend/                  # React application
│   ├── src/                   # Source files
│   ├── public/                # Static assets
│   └── package.json           # NPM dependencies
├── docker-compose.yml         # Multi-container orchestration
├── .github/workflows/         # CI/CD pipelines
├── DEPLOYMENT_GUIDE.md        # Production deployment guide
└── README.md                  # This file
```

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.8+
- Node.js 14+
- PostgreSQL 12+
- Redis 6+

### Quick Start with Docker

```bash
# Clone the repository
git clone https://github.com/maksimmishakov/mismatch-recruiter.git
cd mismatch-recruiter

# Setup environment
cp .env.example .env

# Start services
docker-compose up -d

# Run database migrations
docker-compose exec backend flask db upgrade

# Verify health
curl http://localhost:5000/api/health
```

### Local Development

```bash
# Backend setup
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run migrations
flask db upgrade

# Start development server
flask run

# Frontend setup (in another terminal)
cd frontend
npm install
npm start
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app backend/tests/

# Run specific test file
pytest backend/tests/test_models.py

# Run specific test
pytest backend/tests/test_models.py::TestUserModel::test_user_creation
```

## Database Migrations

```bash
# Create a new migration
flask db migrate -m "Add user table"

# Apply migrations
flask db upgrade

# Revert to previous version
flask db downgrade
```

## API Documentation

### Health Check
```
GET /api/health
```

### Candidates
```
GET /api/candidates              # List all candidates
POST /api/candidates            # Create new candidate
GET /api/candidates/<id>        # Get candidate by ID
PUT /api/candidates/<id>        # Update candidate
DELETE /api/candidates/<id>     # Delete candidate
```

### Jobs
```
GET /api/jobs                    # List all jobs
POST /api/jobs                  # Create new job
GET /api/jobs/<id>              # Get job by ID
PUT /api/jobs/<id>              # Update job
DELETE /api/jobs/<id>           # Delete job
```

### Matches
```
GET /api/matches                 # List all matches
POST /api/matches               # Create new match
GET /api/matches/<id>           # Get match by ID
PUT /api/matches/<id>           # Update match status
```

## Deployment

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for comprehensive production deployment instructions including:

- Docker Compose deployment
- Direct server deployment (Ubuntu/Debian)
- Nginx reverse proxy configuration
- Systemd service setup
- SSL/TLS configuration
- Monitoring and logging
- Backup and recovery procedures

## CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment:

- **backend-test.yml**: Runs Python tests on every push
- **backend-lint.yml**: Checks code quality and style
- **frontend-test.yml**: Runs Node.js tests

Workflows are triggered on:
- Push to main/develop branches
- Pull requests
- Manual workflow dispatch

## Security

- ✅ CSRF protection enabled
- ✅ Secure password hashing with Werkzeug
- ✅ Environment-based configuration
- ✅ SQL injection prevention via ORM
- ✅ Rate limiting
- ✅ HTTPS/TLS support
- ✅ Secrets management

## Configuration

Configuration is managed via environment variables. Copy `.env.example` to `.env` and update with your values:

```bash
FLASK_ENV=production
FLASK_DEBUG=0
SECRET_KEY=<your-secret-key>
DATABASE_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://host:6379/0
```

## Monitoring & Logging

- Application logs in `/var/log/mismatch/`
- Docker logs: `docker-compose logs -f`
- Systemd logs: `journalctl -u mismatch-recruiter -f`
- Sentry integration for error tracking

## Troubleshooting

**Database connection error:**
```bash
# Check database is running
docker-compose ps db

# Recreate database
docker-compose down -v && docker-compose up db
```

**Port already in use:**
```bash
# Find process using port 5000
lsof -i :5000

# Kill process
kill -9 <PID>
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Code Quality Standards

- Python: PEP 8 via `black` and `flake8`
- JavaScript: ESLint configuration included
- Minimum test coverage: 80%
- All PRs must pass CI pipeline

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Authors

- Maksim Mishakov - Initial project setup

## Support

For issues, questions, or suggestions, please:

1. Check existing issues
2. Create a new issue with clear description
3. Include error logs and environment details

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

## Production Status

✅ **PRODUCTION READY**

- [x] Database migrations implemented
- [x] Comprehensive test suite
- [x] CI/CD pipelines configured
- [x] Deployment documentation
- [x] Security best practices
- [x] Performance optimization
- [x] Monitoring setup
