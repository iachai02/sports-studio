.PHONY: docker-up docker-down dev migrate install test lint help

help: ## Lists out all available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

docker-up: ## Starts up docker
	docker compose -f infrastructure/docker/docker-compose.yml up -d

docker-down: ## Closes docker
	docker compose -f infrastructure/docker/docker-compose.yml down

dev: ## Starts backend FastAPI server
	uv run uvicorn api.main:create_app --factory --reload --port 8000

migrate: ## Upgrades alembic head
	cd packages/core/ && uv run alembic upgrade head

install: ## Install all dependencies
	uv sync

test: ## Run all tests
	uv run pytest

lint: ## Checks for all linting errors
	uv run ruff check .
