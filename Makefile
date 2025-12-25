.PHONY: help install test lint format run clean

help:
	@echo "MisMatch Recruitment Bot - Available Commands"
	@echo "install       - Install dependencies from requirements.txt"
	@echo "run           - Run the Flask application"
	@echo "test          - Run pytest unit tests"
	@echo "lint          - Run flake8 code linter"
	@echo "format        - Format code with black and isort"
	@echo "clean         - Clean up __pycache__ and .pytest_cache"

install:
	pip install -r requirements.txt

run:
	python main.py

test:
	pytest tests/ -v --cov=app --cov=services --cov-report=html

lint:
	flake8 app/ services/ utils/ main.py
	black --check .
	isort --check .

format:
	black .
	isort .

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	rm -rf .coverage htmlcov/
