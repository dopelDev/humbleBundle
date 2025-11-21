.PHONY: etl api compose-up compose-down recreate-db recreate-volumes clean-network help

VENV_BIN=.venv/bin
PROJECT_NAME=$(shell basename $(CURDIR) | tr '[:upper:]' '[:lower:]')
NETWORK_NAME=$(PROJECT_NAME)_default
COMPOSE_CMD=docker compose -f docker-compose.dev.yml

etl:
	@$(VENV_BIN)/python -m spider.cli.run_spider

api:
	@$(VENV_BIN)/uvicorn api.main:app --reload

compose-up:
	@$(COMPOSE_CMD) up -d

compose-down:
	@$(COMPOSE_CMD) down

recreate-db:
	@echo "Recreando base de datos..."
	@$(VENV_BIN)/python -c "from spider.database.persistence import recreate_database; from spider.config.settings import get_settings; recreate_database(get_settings())"

recreate-volumes:
	@echo "Eliminando volúmenes..."
	@$(COMPOSE_CMD) down -v
	@echo "Volúmenes eliminados. Ejecuta 'make compose-up' para recrearlos."

clean-network:
	@echo "Deteniendo servicios y eliminando huérfanos..."
	@$(COMPOSE_CMD) down --remove-orphans || true
	@echo "Eliminando red $(NETWORK_NAME)..."
	@if docker network inspect $(NETWORK_NAME) >/dev/null 2>&1; then \
		docker network rm $(NETWORK_NAME) >/dev/null 2>&1 && echo "Red eliminada."; \
	else \
		echo "La red no existe o ya fue eliminada."; \
	fi

help:
	@echo "Comandos disponibles:"
	@echo "  make etl              - Ejecutar ETL para descargar bundles"
	@echo "  make api              - Iniciar servidor API"
	@echo "  make compose-up       - Levantar contenedores Docker"
	@echo "  make compose-down     - Detener contenedores Docker"
	@echo "  make recreate-db      - Recrear base de datos (eliminar y crear tablas)"
	@echo "  make recreate-volumes - Eliminar volúmenes Docker (pgdata e images)"
	@echo "  make clean-network    - Eliminar la red Docker del proyecto"

