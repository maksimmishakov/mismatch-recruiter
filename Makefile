.PHONY: help install test lint format clean docker-build docker-up docker-down db-migrate

help:
	@echo 'MisMatch Recruiter - Available Commands'
	@echo '========================================'
	@echo 'install          - Install dependencies'
	@echo 'test             - Run tests'
	@echo 'test-coverage    - Run tests with coverage report'
	@echo 'lint             - Run linting checks'
	@echo 'format           - Format code'
	@echo 'clean            - Clean temporary files'
	@echo 'docker-build     - Build Docker images'
	@echo 'docker-up        - Start Docker containers'
	@echo 'docker-down      - Stop Docker containers'
	@echo 'db-migrate       - Run database migrations'
	@echo 'dev              - Run development server'
	@echo 'prod             - Run production server'

install:
	cd backend && pip install -r requirements.txt
	cd frontend && npm install

test:
	cd backend && pytest -v

test-coverage:
	cd backend && pytest --cov=app --cov-report=html backend/tests/

test-frontend:
	cd frontend && npm test

lint:
	cd backend && flake8 app/ && black --check app/

format:
	cd backend && black app/ && isort app/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	find . -type d -name '.pytest_cache' -exec rm -rf {} +
	rm -rf frontend/build

dev:
	cd backend && flask run

prod:
	cd backend && gunicorn --workers 4 backend.wsgi:app

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

db-migrate:
	docker-compose exec backend flask db upgrade

db-downgrade:
	docker-compose exec backend flask db downgrade

db-new:
	docker-compose exec backend flask db migrate -m "$(message)"

shell:
	docker-compose exec backend flask shell

check-all: test lint
	echo 'All checks passed!'
