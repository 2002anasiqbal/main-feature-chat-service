
.PHONY: help setup install dev test lint format clean migrate seed docker-build docker-up docker-down

# Default target executed when no arguments are given to make.
help:
	@echo "Available commands:"
	@echo "  setup         Setup the development environment"
	@echo "  install       Install dependencies"
	@echo "  dev           Run the development server"
	@echo "  test          Run tests"
	@echo "  lint          Run linting"
	@echo "  format        Format code"
	@echo "  clean         Clean temporary files"
	@echo "  migrate       Run database migrations"
	@echo "  seed          Seed the database"
	@echo "  docker-build  Build Docker image"
	@echo "  docker-up     Start services with Docker Compose"
	@echo "  docker-down   Stop services"

# Setup development environment
setup: install migrate seed

# Install dependencies
install:
	pip install -r requirements.txt

# Run development server
dev:
	python main.py

# Run tests
test:
	pytest tests/

# Run with coverage
test-cov:
	pytest --cov=src tests/

# Run linting
lint:
	flake8 src/ tests/

# Format code
format:
	black src/ tests/
	isort src/ tests/

# Clean temporary files
clean:
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type d -name "*.egg" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".coverage" -exec rm -r {} +
	find . -type d -name "htmlcov" -exec rm -r {} +
	find . -type d -name "dist" -exec rm -r {} +
	find . -type d -name "build" -exec rm -r {} +

# Run database migrations
migrate:
	alembic upgrade head

# Create a new migration
migration:
	alembic revision --autogenerate -m "$(message)"

# Seed the database
seed:
	python scripts/seed_db.py

# Build Docker image
docker-build:
	docker build -t selgo-boat-service .

# Start services with Docker Compose
docker-up:
	docker-compose up -d

# Start services with Docker Compose (with build)
docker-up-build:
	docker-compose up -d --build

# Follow logs
docker-logs:
	docker-compose logs -f

# Stop services
docker-down:
	docker-compose down

# Remove all Docker volumes
docker-clean:
	docker-compose down -v