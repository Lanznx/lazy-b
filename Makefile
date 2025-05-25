.PHONY: install build run publish version-bump clean

# Helper function to run command with UV or fallback to Python
define run_with_uv_or_python
	@command -v uv >/dev/null 2>&1 && uv run $(1) || $(1)
endef

# Install development dependencies
install:
	@echo "⚙️  Installing dependencies..."
	$(call run_with_uv_or_python,pip install -e ".[dev]")
	@echo "✅ Dependencies installed"

# Build package (includes quality checks)
build: clean
	@echo "🔍 Running quality checks..."
	$(call run_with_uv_or_python,python -m ruff check src/)
	$(call run_with_uv_or_python,python -m mypy src/)
	$(call run_with_uv_or_python,python -m black --check src/)
	@echo "🔨 Building package..."
	$(call run_with_uv_or_python,python -m build)
	@echo "✅ Package built successfully"

# Run LazyB CLI
run:
	@echo "🎭 Starting LazyB CLI..."
	$(call run_with_uv_or_python,python -m src.lazy_b.cli)

# Publish to PyPI
publish: build
	@echo "🚀 Publishing to PyPI..."
	$(call run_with_uv_or_python,python -m twine check dist/*)
	$(call run_with_uv_or_python,python -m twine upload dist/*)
	@echo "✅ Published successfully"

# Update version and create git tag
version-bump:
	@if [ -z "$(VERSION)" ]; then \
		echo "❌ Usage: make version-bump VERSION=x.y.z"; \
		exit 1; \
	fi
	@echo "📝 Updating version to $(VERSION)..."
	@sed -i.bak '/^\[project\]/,/^\[/ s/^version = "[^"]*"/version = "$(VERSION)"/' pyproject.toml
	@sed -i.bak 's/__version__ = "[^"]*"/__version__ = "$(VERSION)"/' src/lazy_b/__init__.py
	@rm -f pyproject.toml.bak src/lazy_b/__init__.py.bak
	@git add pyproject.toml src/lazy_b/__init__.py
	@git commit -m "Bump version to $(VERSION)"
	@git tag -a "v$(VERSION)" -m "Release $(VERSION)"
	@echo "✅ Version $(VERSION) tagged. Push with: git push origin v$(VERSION)"

# Clean build artifacts
clean:
	@rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .mypy_cache/ .ruff_cache/
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true 