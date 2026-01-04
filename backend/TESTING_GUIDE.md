# Testing Guide - Week 3

## Overview
This guide covers testing methodology for the mismatch-recruiter application including unit, integration, and performance testing.

## Test Structure

```
tests/
├── __init__.py
├── conftest.py                    # Shared fixtures
├── unit/
│   ├── __init__.py
│   ├── test_models.py              # Model tests
│   └── test_routes.py              # Route tests
├── integration/
│   ├── __init__.py
│   └── test_workflow.py            # Workflow tests
└── performance/
    ├── __init__.py
    └── test_load.py                # Load tests
```

## Running Tests

### Run All Tests
```bash
pytest
```

### Run Specific Test Suite
```bash
# Unit tests only
pytest tests/unit/ -v

# Integration tests only
pytest tests/integration/ -v

# Performance tests only
pytest tests/performance/ -v
```

### Run with Coverage
```bash
pytest --cov=app --cov-report=html --cov-report=term-missing
```

### Run with Markers
```bash
# Skip slow tests
pytest -m "not slow"

# Run only fast tests
pytest -m "not performance"
```

## Test Coverage

### Current Coverage Targets
- Models: 85%+ coverage
- Routes: 80%+ coverage
- Services: 75%+ coverage
- Overall: 80%+ coverage

### Generate Coverage Report
```bash
pytest --cov=app --cov-report=html
open htmlcov/index.html
```

## Unit Tests

### Model Tests
Testing individual model functionality:
- User creation and authentication
- Candidate data validation
- Job posting functionality
- Match calculation logic

### Route Tests
Testing API endpoints:
- Authentication endpoints
- Candidate management endpoints
- Job management endpoints
- Match endpoints
- Health check endpoints

## Integration Tests

### Workflow Tests
Testing complete user workflows:
- User registration and login
- Creating candidates and jobs
- Matching candidates with jobs
- Viewing match results

### Error Handling Tests
Testing error scenarios:
- Missing authentication
- Invalid data input
- Constraint violations

## Performance Tests

### Load Testing
Ensuring system performs under load:
- Large data sets handling
- Concurrent requests
- Response time requirements
- Database optimization

### Performance Benchmarks
- List endpoints: < 1 second
- Create operations: < 500ms
- Match calculation: < 2 seconds
- Concurrent requests (10): All succeed

## Test Database

### Configuration
Tests use in-memory SQLite database for speed:
```python
DATABASE = 'sqlite:///:memory:'
```

### Fixtures
Common test data fixtures available:
- `test_user`: Pre-created user
- `test_candidate`: Pre-created candidate
- `test_job`: Pre-created job
- `auth_headers`: Authentication headers
- `client`: Test client
- `app`: Flask app instance

## CI/CD Integration

### GitHub Actions Workflow
```yaml
- Run all tests
- Generate coverage reports
- Fail if coverage < 80%
- Performance tests marked as slow
```

## Best Practices

### Writing Tests
1. One assertion per test (when possible)
2. Descriptive test names
3. Use fixtures for setup
4. Test both happy path and edge cases
5. Avoid test interdependencies

### Test Organization
1. Group related tests in classes
2. Use setup and teardown methods
3. Mock external dependencies
4. Keep tests isolated

### Maintenance
1. Update tests when changing code
2. Remove obsolete tests
3. Refactor tests for clarity
4. Keep test data realistic

## Debugging Tests

### Run Single Test
```bash
pytest tests/unit/test_models.py::TestUserModel::test_user_creation -v
```

### Verbose Output
```bash
pytest -vv --tb=long
```

### Stop on First Failure
```bash
pytest -x
```

### Print Debug Info
```bash
pytest -s  # Capture print statements
```

## Common Issues

### Database Errors
Ensure database is created before tests:
```bash
pytest --capture=no
```

### Import Errors
Set PYTHONPATH:
```bash
PYTHONPATH=/workspaces/mismatch-recruiter/backend pytest
```

### Fixture Issues
Check conftest.py is in tests directory

## Coverage Goals by Module

| Module | Target | Current |
|--------|--------|----------|
| models.py | 85% | - |
| routes/ | 80% | - |
| schemas.py | 90% | - |
| services/ | 75% | - |
| utils/ | 70% | - |
| Overall | 80% | - |

## Test Metrics

### Track These Metrics
- Test execution time
- Code coverage percentage
- Test pass rate
- Failure analysis
- Performance regressions

## Next Steps

1. Expand test coverage to 90%
2. Add API contract testing
3. Implement load testing with realistic data
4. Add security testing
5. Implement mutation testing

---
Testing Guide - Week 3
Last Updated: January 10, 2025

