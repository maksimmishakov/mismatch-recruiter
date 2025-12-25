# Testing Guide for Lamoda AI Recruiter

## Quick Start

```bash
# Install dependencies
pip install pytest pytest-cov redis

# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ -v --cov=app --cov=services

# Run specific test file
pytest tests/test_api_endpoints.py -v

# Run specific test class
pytest tests/test_api_endpoints.py::TestHealthCheckEndpoint -v

# Run specific test
pytest tests/test_api_endpoints.py::TestHealthCheckEndpoint::test_health_check_returns_200 -v
```

## Test Structure

### test_api_endpoints.py
Comprehensive API endpoint testing:
- **TestHealthCheckEndpoint**: Health check endpoint validation
- **TestAuthEndpoints**: Authentication endpoints (register, login)
- **TestCandidatesEndpoint**: Candidate management and filtering
- **TestSalaryPredictionEndpoint**: Salary prediction service
- **TestMatchResume ToJobEndpoint**: Resume-to-job matching

### test_performance.py
Performance and load testing:
- **TestResponseTimeOptimization**: API response time verification
- **TestDatabaseQueryPerformance**: Query execution time testing
- **TestCachePerformance**: Cache hit ratio and performance
- **TestLoadTesting**: Concurrent user load testing
- **TestDatabaseConnectionPooling**: Connection pool validation

## Running Tests

### Unit Tests
```bash
# Run API endpoint tests
pytest tests/test_api_endpoints.py -v

# Expected output:
# test_health_check_returns_200 PASSED
# test_register_success PASSED
# test_login_success PASSED
# ... (15+ more tests)
```

### Performance Tests
```bash
# Run performance tests
pytest tests/test_performance.py -v

# Tests validate:
# - Health check < 50ms
# - Cached endpoints < 100ms
# - DB queries < 10ms (simple), < 50ms (JOINs)
# - Cache hit ratio > 80%
# - 100 concurrent users: 95%+ success rate
# - 500 concurrent users: 90%+ success rate
```

## Requirements

### Services Running
- PostgreSQL database
- Redis cache server
- Flask application on localhost:5000

### Dependencies
```
pytest>=7.0.0
pytest-cov>=4.0.0
redis>=4.3.4
requests>=2.28.0
concurrent-futures (built-in for Python 3.7+)
```

## Continuous Integration

Tests run automatically on:
- Push to master/develop branches
- Pull requests

CI Configuration: `.github/workflows/comprehensive_ci.yml`

## Coverage Requirements

- **Minimum coverage**: 80%
- **Target coverage**: 95%

Check coverage:
```bash
pytest tests/ --cov=app --cov=services --cov-report=html
open htmlcov/index.html
```

## Debugging Tests

### Enable SQL logging
```python
app.config['SQLALCHEMY_ECHO'] = True
```

### Print debug info
```bash
pytest tests/test_api_endpoints.py -v -s
```

### Run single test with breakpoint
```bash
pytest tests/test_api_endpoints.py::TestAuthEndpoints::test_login_success -v -s --pdb
```

## Performance Baselines

| Endpoint | Type | Target | Actual |
|----------|------|--------|--------|
| /api/health | GET | < 50ms | TBD |
| /api/candidates | GET | < 100ms | TBD |
| /api/salary-prediction | POST | < 500ms | TBD |
| Database (simple) | Query | < 10ms | TBD |
| Database (JOIN) | Query | < 50ms | TBD |

## Test Checklist

- [ ] Health check endpoint returns 200
- [ ] Authentication endpoints validate input
- [ ] JWT tokens work correctly
- [ ] Candidates endpoint requires auth
- [ ] Pagination works
- [ ] Filtering works
- [ ] Salary prediction handles edge cases
- [ ] Resume matching returns valid scores
- [ ] Cache hit ratio > 80%
- [ ] Response times meet targets
- [ ] 100 concurrent users: 95%+ success
- [ ] 500 concurrent users: 90%+ success

## Troubleshooting

### Redis not available
```
redis.ConnectionError: Cannot connect to Redis
```
Solution: Start Redis server
```bash
redis-server
```

### Database errors
```
SQLAlchemy operational error
```
Solution: Ensure PostgreSQL is running and migrations applied
```bash
flask db upgrade
```

### Import errors
```bash
# Install missing dependencies
pip install -r requirements.txt
```

## Contributing

When adding new features:
1. Write tests first (TDD)
2. Ensure all tests pass
3. Maintain 95%+ coverage
4. Performance targets met
5. Create PR with test results
