.PHONY: docker-up docker-down dev

docker-up:
	docker compose -f infrastructure/docker/docker-compose.yml up -d

docker-down:
	docker compose -f infrastructure/docker/docker-compose.yml down

dev:
	uv run uvicorn api.main:create_app --factory --reload --port 8000

