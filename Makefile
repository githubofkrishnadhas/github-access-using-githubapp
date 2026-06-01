# Default target
.DEFAULT_GOAL := help

# Variables
UV := uv

.PHONY: help install sync update tree add remove uninstall clean run lock

help: ## Show available commands
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

install: ## Install dependencies from pyproject.toml
	$(UV) sync

sync: ## Sync environment with lock file
	$(UV) sync

update: ## Update dependencies
	$(UV) lock --upgrade
	$(UV) sync

tree: ## Show dependency tree
	$(UV) tree

lock: ## Generate/update uv.lock
	$(UV) lock

add: ## Add a package (usage: make add package=requests)
	$(UV) add $(package)

remove: ## Remove a package (usage: make remove package=requests)
	$(UV) remove $(package)

uninstall: ## Alias for remove
	$(UV) remove $(package)

run: ## Run python app (usage: make run script=main.py)
	$(UV) run python $(script)

clean: ## Remove virtual environment and cache
	rm -rf .venv
	rm -rf .pytest_cache
	rm -rf __pycache__
	find . -type d -name "__pycache__" -exec rm -rf {} +