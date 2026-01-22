.PHONY: lint typecheck test e2e up down migrate

lint:
	ruff check .

typecheck:
	mypy .

test:
	pytest -q

e2e:
	python scripts/simulate_flow.py

migrate:
	alembic upgrade head

up:
	docker compose -f docker-compose.dev.yml up -d

down:
	docker compose -f docker-compose.dev.yml down
