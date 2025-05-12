.PHONY: clean lint test build install all release

all: clean lint test build

clean:
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .coverage htmlcov/ .mypy_cache/ .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +

lint:
	ruff src/ tests/
	mypy src/
	black --check src/ tests/

format:
	black src/ tests/
	ruff --fix src/ tests/

build:
	python -m build

install:
	pip install -e ".[dev]"

dev-setup:
	pip install -U pip
	pip install -e ".[dev]" 

release:
	@echo "Current version: $$(grep -o 'version = "[^"]*"' pyproject.toml | cut -d'"' -f2)"
	@read -p "Enter new version (e.g., 0.2.0): " version; \
	python scripts/update_version.py $$version 