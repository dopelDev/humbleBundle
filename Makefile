.PHONY: etl api compose-up compose-down recreate-db recreate-volumes clean-network frontend-build frontend-dev api-rebuild help

VENV_BIN=.venv/bin
PROJECT_NAME=$(shell basename $(CURDIR) | tr '[:upper:]' '[:lower:]')
NETWORK_NAME=$(PROJECT_NAME)_default
COMPOSE_CMD=docker compose -f docker-compose.dev.yml

etl:
	@$(VENV_BIN)/python -m spider.cli.run_spider

api:
	@$(COMPOSE_CMD) restart api

compose-up:
	@$(COMPOSE_CMD) up -d

compose-down:
	@$(COMPOSE_CMD) down

recreate-db:
	@echo "Recreando base de datos vía Docker (drop de volumen pgdata)..."
	@$(COMPOSE_CMD) down -v --remove-orphans
	@docker volume rm -f $(PROJECT_NAME)_pgdata >/dev/null 2>&1 || true
	@$(COMPOSE_CMD) up -d postgres

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

frontend-build:
	@cd frontend && npm run build

frontend-dev:
	@cd frontend && npm run dev

api-rebuild:
	@echo "Rebuild + restart del servicio API..."
	@$(COMPOSE_CMD) up -d --build api

help:
	@echo "Comandos disponibles:"
	@echo "  make etl              - Ejecutar ETL para descargar bundles"
	@echo "  make api              - Iniciar servidor API"
	@echo "  make compose-up       - Levantar contenedores Docker"
	@echo "  make compose-down     - Detener contenedores Docker"
	@echo "  make recreate-db      - Dropea volumen pgdata y levanta postgres limpio"
	@echo "  make recreate-volumes - Eliminar volúmenes Docker (pgdata e images)"
	@echo "  make clean-network    - Eliminar la red Docker del proyecto"
	@echo "  make frontend-build   - Ejecutar 'npm run build' en frontend/"
	@echo "  make frontend-dev     - Ejecutar 'npm run dev' en frontend/"
	@echo "  make api-rebuild      - Rebuild y restart del contenedor API"
