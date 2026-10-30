.PHONY: help install dev-install test lint format audit build clean

help:
	@echo "Available commands:"
	@echo "  make install      Install haunted-shell in current environment"
	@echo "  make dev-install  Install in editable mode with development & testing tools"
	@echo "  make test         Run test suite with pytest"
	@echo "  make lint         Run flake8 lint checks"
	@echo "  make format       Format code with black"
	@echo "  make audit        Run pip-audit vulnerability scanner"
	@echo "  make build        Build sdist and wheel packages"
	@echo "  make clean        Remove build artifacts and bytecode caches"

install:
	pip install -r requirements.txt
	pip install .

dev-install:
	pip install -r requirements.txt
	pip install -e ".[dev]"

test:
	pytest tests/

lint:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --exclude=.venv

format:
	black haunted_shell tests

audit:
	pip-audit -r requirements.txt

build:
	python -m build

clean:
	rm -rf dist/ build/ *.egg-info/ .pytest_cache/ .coverage htmlcov/
	find . -type d -name "__pycache__" -exec rm -rf {} +
