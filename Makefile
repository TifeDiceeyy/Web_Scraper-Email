.PHONY: help install install-dev test test-cov lint format clean run validate

help:
	@echo "Business Outreach Automation - Available Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install       Install production dependencies"
	@echo "  make install-dev   Install development dependencies"
	@echo "  make validate      Validate environment variables"
	@echo ""
	@echo "Development:"
	@echo "  make test          Run tests"
	@echo "  make test-cov      Run tests with coverage report"
	@echo "  make lint          Run linters (flake8, pylint)"
	@echo "  make format        Format code with black"
	@echo "  make clean         Remove cache and build files"
	@echo ""
	@echo "Running:"
	@echo "  make run           Start the agent"
	@echo ""

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

validate:
	python validate_env.py

test:
	pytest

test-cov:
	pytest --cov=tools --cov=validators --cov=logger --cov=constants --cov-report=html --cov-report=term
	@echo ""
	@echo "Coverage report generated in htmlcov/index.html"

lint:
	@echo "Running flake8..."
	flake8 tools/ validators.py logger.py constants.py agent.py --max-line-length=100 --ignore=E501,W503
	@echo ""
	@echo "Running pylint..."
	pylint tools/ validators.py logger.py constants.py agent.py --disable=C0111,C0103,R0913,R0914,W0703 || true

format:
	black tools/ tests/ validators.py logger.py constants.py agent.py --line-length=100

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete
	find . -type f -name '*.log' -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf build dist *.egg-info
	@echo "Cleaned up cache and build files"

run:
	python agent.py

# Shortcuts
t: test
tc: test-cov
l: lint
f: format
c: clean
r: run
v: validate
