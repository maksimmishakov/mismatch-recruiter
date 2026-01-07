# Testing Guide

## Test Structure
Tests are organized by module:
- `backend/tests/conftest.py` - Pytest fixtures
- `backend/tests/test_auth.py` - Authentication tests
- `backend/tests/test_candidates.py` - Candidate endpoints tests

## Running Tests
```bash
# Run all tests
pytest backend/tests -v

# Run specific test file
pytest backend/tests/test_auth.py -v

# Run with coverage
pytest backend/tests --cov=app --cov-report=html
```

## Test Coverage Goals
- Unit tests: 80%+ coverage
- Integration tests: 60%+ coverage
- Critical paths: 100% coverage
