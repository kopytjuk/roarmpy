publish-testpypi: build ## Publish to pypi
	@echo "🚀 Publishing project"
	$(eval user := $(shell sed -ne 's/username *= *//p' .pypirc))
	$(eval pass := $(shell sed -ne 's/password *= *//p' .pypirc))
	uv publish -u $(user) -p $(pass) --index testpypi

.PHONY: build
build: clean-build ## Build wheel file
	@echo "🚀 Creating wheel file"
	uv build

.PHONY: clean-build
clean-build: ## Clean build artifacts
	@echo "🚀 Removing build artifacts"
	uv run python -c "import shutil; import os; shutil.rmtree('dist') if os.path.exists('dist') else None"