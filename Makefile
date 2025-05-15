DOCKER_COMP = docker compose -f docker-compose.yaml
MANAGER = $(DOCKER_COMP) exec backend uv run 

up:
	@$(DOCKER_COMP) up --detach --wait

down:
	@$(DOCKER_COMP) down --remove-orphans

bash:
	@$(DOCKER_COMP) exec $(name) bash

migrations:
	@$(MANAGER) alembic revision --autogenerate -m "Initial migration"

rollback:
	@$(MANAGER) alembic downgrade base

migrate:
	@$(MANAGER) alembic upgrade head

logs:
	@$(DOCKER_COMP) logs $(name) --tail=0 --follow

linter:
	@uv run black .