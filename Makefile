.DEFAULT_GOAL := help
.PHONY: help install test lint fmt run docs docker-build docker-up zip

help:  ## Show this help
	@grep -E '^[a-z-]+:.*##' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  %-14s %s\n", $$1, $$2}'

install:  ## Install in editable mode with dev tools
	pip install -e ".[dev]"

test:  ## Run the test suite
	python -m pytest -q

lint:  ## Lint with ruff
	ruff check .

fmt:  ## Auto-fix lint issues
	ruff check --fix .

run:  ## Run over stdio (local)
	python -m daily_tutor

docs:  ## Regenerate docs/TOOLS.md from the server's tool docstrings
	python scripts/gen_tools_doc.py

docker-build:  ## Build the Docker image
	docker build -t daily-tutor-mcp .

docker-up:  ## Start with docker compose (needs .env)
	docker compose up -d --build

zip:  ## Create a clean release archive
	git archive --format=zip --prefix=daily-tutor-mcp/ -o daily-tutor-mcp.zip HEAD
