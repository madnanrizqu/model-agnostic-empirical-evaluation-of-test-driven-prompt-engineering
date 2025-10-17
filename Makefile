
# Convenience Makefile for pyenv + Poetry workflow
# Usage: make <target>

SHELL = /bin/bash
.ONESHELL:
.DEFAULT_GOAL := help
POETRY ?= poetry

# Colors
CYAN=\033[36m
NC=\033[0m

help: ## Show available Make targets
	@echo "Available targets:" && \
	awk -F':|##' '/^[a-zA-Z0-9_.\-]+:.*##/ {printf "  $(CYAN)%-22s$(NC) %s\n", $$1, $$3}' $(MAKEFILE_LIST)

setup: ## Does everything for new users (requires Poetry to be installed)
		@echo "==> Starting one-shot setup"
		@if command -v $(POETRY) >/dev/null 2>&1; then \
				POETRY_BIN=$$(command -v $(POETRY)); \
		elif [ -x "$$HOME/.local/bin/poetry" ]; then \
				POETRY_BIN="$$HOME/.local/bin/poetry"; \
		else \
				echo "Poetry not found."; \
				echo "Install Poetry, then re-run: make setup"; \
				exit 1; \
		fi; \
		echo "Using Poetry: $$($$POETRY_BIN --version)"; \
		$$POETRY_BIN config virtualenvs.in-project true; \
		echo "Configured Poetry to use .venv in project"; \
		if command -v pyenv >/dev/null 2>&1; then \
				PY=$$(pyenv which python); echo "Using pyenv python: $$PY"; \
		else \
				PY=$$(command -v python); echo "Using system python: $$PY"; \
		fi; \
		$$POETRY_BIN env use "$$PY"; \
		$$POETRY_BIN install; \
		echo "==> Setup complete"; \
		echo "To activate the environment now:"; \
		echo "  source $$($$POETRY_BIN env info --path)/bin/activate"; \
		echo "Or run scripts with:"; \
		echo "  $$POETRY_BIN run python path/to/script.py"

activate-cmd: ## Print the command to activate the Poetry venv in your current shell
	@echo "Run this to activate the environment in your current shell:"
	@echo "source $$($(POETRY) env info --path)/bin/activate"

.PHONY: help setup activate-cmd
