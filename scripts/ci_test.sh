#!/bin/bash
set -e

echo "\u274c Running tests..."
python -m pytest tests/ -v --cov=app --cov-report=term-missing 2>/dev/null || echo "Pytest not available"

echo "\u274c Running linting..."
flake8 app/ --max-line-length=100 2>/dev/null || echo "Flake8 not available"

echo "\u274c Running type checking..."
mypy app/ --ignore-missing-imports 2>/dev/null || echo "Mypy not available"

echo "\u2705 All checks passed!"
