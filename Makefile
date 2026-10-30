.PHONY: help install dev-install test test-cov lint typecheck format audit build check clean

help:
	@echo "haunted-shell - Production Developer Commands:"
	@echo "  make install      Install haunted-shell in current environment"
	@echo "  make dev-install  Install in editable mode with development & testing tools"
	@echo "  make test         Run test suite with pytest"
	@echo "  make test-cov     Run test suite with coverage report"
	@echo "  make lint         Run lint checks with ruff"
	@echo "  make typecheck    Run strict type checking with mypy"
	@echo "  make format       Format code and organize imports with ruff"
	@echo "  make audit        Run pip-audit vulnerability scanner"
	@echo "  make check        Run lint, typecheck, and tests in sequence"
	@echo "  make build        Build sdist and wheel packages"
	@echo "  make clean        Remove build artifacts and bytecode caches"

install:
	pip install -r requirements.txt
	pip install .

dev-install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pip install --no-build-isolation -e ".[dev]"

test:
	pytest tests/

test-cov:
	pytest --cov=haunted_shell --cov-report=term-missing tests/

lint:
	ruff check haunted_shell tests

typecheck:
	mypy haunted_shell

format:
	ruff format haunted_shell tests
	ruff check --fix haunted_shell tests

audit:
	pip-audit -r requirements.txt

check: lint typecheck test

build:
	python3 -m pip install --upgrade build
	python3 -m build

clean:
	rm -rf dist/ build/ *.egg-info/ .pytest_cache/ .coverage htmlcov/ .mypy_cache/ .ruff_cache/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.py[cod]" -delete
