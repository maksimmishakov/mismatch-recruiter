# Production Readiness Checklist

## Infrastructure
- [ ] `docker-compose up --build` успешно на чистой машине
- [ ] Backend отвечает на GET /health -> 200 ✓
- [ ] Frontend доступен на http://localhost:3000
- [ ] PostgreSQL поднимается и инициализируется
- [ ] All environment variables configured

## CI/CD Pipelines
- [ ] GitHub Actions backend-test.yml зелёный ✓
- [ ] GitHub Actions backend-lint.yml зелёный ✓
- [ ] GitHub Actions frontend-test.yml зелёный ✓
- [ ] GitHub Actions amvera-deploy.yml ready
- [ ] Deployment workflow tested and working

## Testing
- [ ] Backend tests: pytest --cov=app ≥ 50%
- [ ] Frontend build: npm run build без ошибок
- [ ] Locust load test: 50+ users, <500ms avg response
- [ ] All API endpoints return expected status codes
- [ ] Health check endpoint working

## Code Quality
- [ ] No linting errors (flake8, black, isort)
- [ ] Type hints added where applicable
- [ ] Docstrings for all public functions
- [ ] Requirements.txt updated and verified
- [ ] .env.example contains all needed variables

## Security
- [ ] No secrets in code or commits
- [ ] JWT tokens properly configured
- [ ] CORS whitelisted correctly
- [ ] HTTPS/SSL ready for production
- [ ] Database credentials in secrets, not code

## Documentation
- [ ] README.md complete and accurate
- [ ] DEPLOYMENT_GUIDE.md created
- [ ] API.md or Swagger documentation available
- [ ] Architecture diagram documented
- [ ] Setup instructions tested on clean machine

## Database
- [ ] Alembic migrations working
- [ ] Initial migration created and tested
- [ ] Database backup procedures documented
- [ ] Migration rollback tested

## Deployment
- [ ] Amvera environment secrets configured
- [ ] Health checks defined in amvera.yml
- [ ] Auto-deployment on main push enabled
- [ ] Monitoring and alerting ready
- [ ] Rollback procedures documented

## Demo Preparation
- [ ] Demo script prepared (5-7 min)
- [ ] Test credentials ready
- [ ] Screenshots/recordings captured
- [ ] Presentation slides prepared
- [ ] Live demo tested end-to-end

## Sign-Off
- [ ] Tech Lead review completed
- [ ] All checklist items verified
- [ ] Ready for production deployment

Last updated: $(date '+%Y-%m-%d %H:%M:%S')
