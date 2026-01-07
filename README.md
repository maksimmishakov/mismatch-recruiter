# MisMatch Recruiter - Modern Job Matching Platform

## Overview

MisMatch Recruiter is a sophisticated job matching platform built with modern technologies:
- **Backend**: Flask with SQLAlchemy ORM
- **Frontend**: React 18 with Axios
- **Database**: PostgreSQL
- **Infrastructure**: Docker & Docker Compose
- **CI/CD**: GitHub Actions

## Project Structure

```
mismatch-recruiter/
├── backend/                      # Flask backend
│   ├── app/
│   │   ├── __init__.py          # App factory
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── routes.py        # API endpoints
│   │   ├── config/
│   │   │   ├── __init__.py
│   │   │   ├── development.py
│   │   │   ├── production.py
│   │   │   └── testing.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── job_posting.py
│   │   │   ├── candidate.py
│   │   │   └── match.py
│   │   ├── services/
│   │   ├── utils/
│   │   └── tests/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── main.py
├── frontend/                     # React frontend
│   ├── src/
│   │   ├── App.js
│   │   ├── index.js
│   │   └── components/
│   ├── public/
│   │   └── index.html
│   ├── package.json
│   └── Dockerfile
├── .github/
│   └── workflows/
│       ├── backend.yml          # Backend CI/CD
│       └── frontend.yml         # Frontend CI/CD
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

## Prerequisites

- Docker & Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local backend development)
- PostgreSQL 15+ (or use Docker)

## Getting Started

### Option 1: Using Docker Compose (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/your-username/mismatch-recruiter.git
cd mismatch-recruiter
```

2. Create environment file:
```bash
cp .env.example .env
```

3. Build and start containers:
```bash
docker-compose up --build
```

4. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000/api
- Database: localhost:5432

### Option 2: Local Development

#### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example ../.env
python main.py
```

#### Frontend Setup

```bash
cd frontend
npm install
npm start
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user

### Health
- `GET /api/health` - API health check

## Database Models

### User
- Stores user account information
- Fields: id, email, username, hashed_password, full_name, role, is_active, created_at

### Candidate
- Job candidate profiles
- Fields: id, first_name, last_name, email, skills, experience_years, github_url, linkedin_url, etc.

### JobPosting
- Job opportunities
- Fields: id, title, description, company, location, salary_min, salary_max, required_skills, etc.

### Match
- Matches between candidates and jobs
- Fields: id, candidate_id, job_posting_id, match_score, skill_match, experience_match, location_match, status

## CI/CD Pipeline

### Backend Tests
- Runs on: Python 3.11, PostgreSQL 15
- Tests: pytest with coverage
- Linting: flake8
- Triggers: Push/PR to main or develop, changes in backend/ directory

### Frontend Tests
- Runs on: Node.js 18
- Build: React build process
- Artifacts: Upload build files
- Triggers: Push/PR to main or develop, changes in frontend/ directory

## Configuration

### Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:password@host:5432/database
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_PORT=5000

# Security
JWT_SECRET_KEY=your-secret-key-here

# Frontend
REACT_APP_API_URL=http://localhost:5000/api
```

## Development Workflow

1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes and commit: `git commit -am 'Add new feature'`
3. Push to GitHub: `git push origin feature/your-feature`
4. Create Pull Request on GitHub
5. CI/CD pipeline runs automatically
6. Merge when tests pass

## Deployment

### Production Deployment

1. Update production environment variables
2. Build Docker images:
```bash
docker build -t mismatch-recruiter-backend backend/
docker build -t mismatch-recruiter-frontend frontend/
```

3. Push to container registry (Docker Hub, ECR, etc.)
4. Deploy using orchestration tool (Docker Swarm, Kubernetes, etc.)

## Testing

### Backend Tests
```bash
cd backend
pytest
pytest --cov=app  # With coverage
```

### Frontend Tests
```bash
cd frontend
npm test
npm run build  # Build for production
```

## Security Considerations

- JWT tokens for API authentication
- Password hashing with bcrypt
- CORS protection
- Environment variable secrets management
- SQL injection prevention via ORM
- Input validation on all endpoints

## Performance Optimization

- Database indexing on frequently queried columns
- PostgreSQL connection pooling
- React component lazy loading
- API response caching
- Production-grade WSGI server (Gunicorn)

## Monitoring & Logging

- Application logging
- Error tracking
- Performance metrics
- API response times

## Contributing

1. Fork the repository
2. Create feature branch
3. Follow code style guidelines
4. Write tests for new features
5. Submit pull request

## License

MIT License - See LICENSE file for details

## Support

For issues, feature requests, or questions:
- GitHub Issues: https://github.com/your-username/mismatch-recruiter/issues
- Email: support@mismatchrecruiter.com
