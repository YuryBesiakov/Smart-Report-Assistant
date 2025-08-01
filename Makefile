# Smart Report Assistant - Development Makefile

.PHONY: help install install-dev test test-all test-integration test-cov test-cov-all lint format clean docker-build docker-run setup

# Default target
help:
	@echo "Smart Report Assistant - Available commands:"
	@echo "  install          - Install production dependencies"
	@echo "  install-dev      - Install development dependencies"
	@echo "  setup            - Set up development environment"
	@echo "  test             - Run unit tests (excludes integration tests)"
	@echo "  test-all         - Run all tests including integration tests"
	@echo "  test-integration - Run integration tests only (requires API key)"
	@echo "  test-cov         - Run unit tests with coverage"
	@echo "  test-cov-all     - Run all tests with coverage"
	@echo "  lint             - Run linting checks"
	@echo "  format           - Format code with black and isort"
	@echo "  clean            - Clean up generated files"
	@echo "  docker-build     - Build Docker image"
	@echo "  docker-run       - Run application in Docker"
	@echo "  security         - Run security checks"
	@echo "  ci               - Run all CI checks locally"

# Installation
install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

# Development setup
setup: install-dev
	pre-commit install
	@echo "Development environment setup complete!"

# Testing
test:
	pytest tests/ -v -m "not integration"

test-all:
	pytest tests/ -v

test-integration:
	pytest tests/ -v -m integration

test-cov:
	pytest tests/ -v --cov=app --cov-report=html --cov-report=term -m "not integration"

test-cov-all:
	pytest tests/ -v --cov=app --cov-report=html --cov-report=term

# Code quality
lint:
	flake8 app/ tests/
	mypy app/ --ignore-missing-imports
	bandit -r app/

format:
	black app/ tests/
	isort app/ tests/

# Security
security:
	bandit -r app/ -f json -o bandit-report.json
	safety check

# Docker
docker-build:
	docker build -t smart-report-assistant .

docker-run:
	docker run -p 5000:5000 smart-report-assistant

docker-compose-dev:
	docker-compose up --build

docker-compose-prod:
	docker-compose --profile production up --build

# Cleanup
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf htmlcov/
	rm -f .coverage
	rm -f bandit-report.json
	rm -f safety-report.json

# CI/CD simulation
ci: lint test security
	@echo "All CI checks passed!"

# Local development server
dev:
	python app/main.py

# Production server (using gunicorn)
prod:
	pip install gunicorn
	gunicorn --bind 0.0.0.0:5000 app.main:app
