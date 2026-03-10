.PHONY: help install install-dev test coverage lint format run clean

help:
	@echo "MisMatch Recruitment Bot - Available Commands"
	@echo "install      - Install production dependencies from requirements.txt"
	@echo "install-dev  - Install dev dependencies (requirements-dev.txt)"
	@echo "run          - Run the Flask application via wsgi.py"
	@echo "test         - Run pytest unit tests with coverage"
	@echo "coverage     - Run tests and show term-missing coverage report"
	@echo "lint         - Run flake8 + black --check + isort --check"
	@echo "format       - Format code with black and isort"
	@echo "clean        - Clean up __pycache__ and .pytest_cache"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

run:
	python wsgi.py

test:
	pytest tests/ -v --cov=app --cov=services --cov-report=html --cov-report=term

coverage:
	pytest tests/ -v --cov=app --cov=services --cov=utils --cov-report=term-missing

lint:
	flake8 app/ services/ utils/ main.py wsgi.py
	black --check .
	isort --check .

format:
	black .
	isort .

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	rm -rf .coverage htmlcov/
	rm -rf bandit-report.json safety-report.json
