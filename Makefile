
# Convenience Makefile for all important workflows of the codebase
# Usage: make <target>

SHELL = /bin/bash
.ONESHELL:
.DEFAULT_GOAL := help
POETRY ?= poetry
PORT ?= 8000
DOCKER_IMAGE ?= llm-evaluation-system

# Colors
CYAN=\033[36m
GREEN=\033[32m
YELLOW=\033[33m
NC=\033[0m

help: ## Show available Make targets
	@echo "$(GREEN)Available targets:$(NC)" && \
	awk -F':|##' '/^[a-zA-Z0-9_.\-]+:.*##/ {printf "  $(CYAN)%-22s$(NC) %s\n", $$1, $$3}' $(MAKEFILE_LIST)

# ============================================================================
# Setup & Environment
# ============================================================================

setup: ## Does everything for new users (requires Poetry to be installed)
		@echo "$(GREEN)==> Starting one-shot setup$(NC)"
		@if command -v $(POETRY) >/dev/null 2>&1; then \
				POETRY_BIN=$$(command -v $(POETRY)); \
		elif [ -x "$$HOME/.local/bin/poetry" ]; then \
				POETRY_BIN="$$HOME/.local/bin/poetry"; \
		else \
				echo "$(YELLOW)Poetry not found.$(NC)"; \
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
		echo "$(GREEN)==> Setup complete$(NC)"; \
		echo "To activate the environment now:"; \
		echo "  source $$($$POETRY_BIN env info --path)/bin/activate"; \
		echo "Or run scripts with:"; \
		echo "  $$POETRY_BIN run python path/to/script.py"

activate-cmd: ## Print the command to activate the Poetry venv in your current shell
	@echo "$(GREEN)Run this to activate the environment in your current shell:$(NC)"
	@echo "source $$($(POETRY) env info --path)/bin/activate"

# ============================================================================
# Local Experiments (Poetry)
# ============================================================================

rq1: ## Run all RQ1 experiments locally
	@echo "$(GREEN)==> Running all RQ1 experiments$(NC)"
	$(POETRY) run python rq1/run_all.py

rq1-exp: ## Run specific RQ1 experiment (make rq1-exp EXP=<name>)
	@if [ -z "$(EXP)" ]; then \
		echo "$(YELLOW)Error: EXP variable required$(NC)"; \
		echo "Usage: make rq1-exp EXP=human_eval_chatgpt4o"; \
		exit 1; \
	fi
	@echo "$(GREEN)==> Running RQ1 experiment: $(EXP)$(NC)"
	$(POETRY) run python rq1/run_all.py --folders $(EXP)

rq2: ## Run all RQ2 experiments locally
	@echo "$(GREEN)==> Running all RQ2 experiments$(NC)"
	$(POETRY) run python rq2/run_all.py

rq2-exp: ## Run specific RQ2 experiment (make rq2-exp EXP=<name>)
	@if [ -z "$(EXP)" ]; then \
		echo "$(YELLOW)Error: EXP variable required$(NC)"; \
		echo "Usage: make rq2-exp EXP=code_contests_chatgpt4o"; \
		exit 1; \
	fi
	@echo "$(GREEN)==> Running RQ2 experiment: $(EXP)$(NC)"
	$(POETRY) run python rq2/run_all.py --folders $(EXP)

# ============================================================================
# Docker
# ============================================================================

docker-build: ## Build Docker image
	@echo "$(GREEN)==> Building Docker image$(NC)"
	docker build -t $(DOCKER_IMAGE) .

docker-rq1: docker-build ## Run RQ1 experiments in Docker (with config & results persistence)
	@echo "$(GREEN)==> Running RQ1 in Docker$(NC)"
	docker run \
		-v $(PWD)/.env:/app/.env \
		-v $(PWD)/config:/app/config \
		-v $(PWD)/rq1:/app/rq1 \
		$(DOCKER_IMAGE) \
		poetry run python rq1/run_all.py

docker-rq1-exp: docker-build ## Run specific RQ1 in Docker (make docker-rq1-exp EXP=<name>)
	@if [ -z "$(EXP)" ]; then \
		echo "$(YELLOW)Error: EXP variable required$(NC)"; \
		echo "Usage: make docker-rq1-exp EXP=human_eval_chatgpt4o"; \
		exit 1; \
	fi
	@echo "$(GREEN)==> Running RQ1 experiment in Docker: $(EXP)$(NC)"
	docker run \
		-v $(PWD)/.env:/app/.env \
		-v $(PWD)/config:/app/config \
		-v $(PWD)/rq1:/app/rq1 \
		$(DOCKER_IMAGE) \
		poetry run python rq1/run_all.py --folders $(EXP)

docker-rq2: docker-build ## Run RQ2 experiments in Docker (with config & results persistence)
	@echo "$(GREEN)==> Running RQ2 in Docker$(NC)"
	docker run \
		-v $(PWD)/.env:/app/.env \
		-v $(PWD)/config:/app/config \
		-v $(PWD)/rq2:/app/rq2 \
		$(DOCKER_IMAGE) \
		poetry run python rq2/run_all.py

docker-rq2-exp: docker-build ## Run specific RQ2 in Docker (make docker-rq2-exp EXP=<name>)
	@if [ -z "$(EXP)" ]; then \
		echo "$(YELLOW)Error: EXP variable required$(NC)"; \
		echo "Usage: make docker-rq2-exp EXP=code_contests_chatgpt4o"; \
		exit 1; \
	fi
	@echo "$(GREEN)==> Running RQ2 experiment in Docker: $(EXP)$(NC)"
	docker run \
		-v $(PWD)/.env:/app/.env \
		-v $(PWD)/config:/app/config \
		-v $(PWD)/rq2:/app/rq2 \
		$(DOCKER_IMAGE) \
		poetry run python rq2/run_all.py --folders $(EXP)

docker-shell: docker-build ## Start interactive Docker shell
	@echo "$(GREEN)==> Starting Docker shell$(NC)"
	docker run -it \
		-v $(PWD)/.env:/app/.env \
		-v $(PWD)/config:/app/config \
		-v $(PWD)/rq1:/app/rq1 \
		-v $(PWD)/rq2:/app/rq2 \
		$(DOCKER_IMAGE) \
		/bin/bash

docker-clean: ## Remove Docker image
	@echo "$(YELLOW)==> Removing Docker image$(NC)"
	docker rmi $(DOCKER_IMAGE) || true

# ============================================================================
# Utilities
# ============================================================================

serve: ## Serve docs/ locally at http://localhost:$(PORT)
	@if command -v python3 >/dev/null 2>&1; then PY=python3; else PY=python; fi; \
		echo "Using $$PY"; \
		echo "$(GREEN)Serving docs/ at http://localhost:$(PORT)$(NC) (Ctrl+C to stop)"; \
		cd docs; \
		$$PY -m http.server $(PORT)

.PHONY: help setup activate-cmd rq1 rq1-exp rq2 rq2-exp docker-build docker-rq1 docker-rq1-exp docker-rq2 docker-rq2-exp docker-shell docker-clean serve
