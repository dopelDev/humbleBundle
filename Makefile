.PHONY: etl api db-init db-reset frontend-build frontend-dev docker-up docker-down docker-restart help

VENV_BIN=.venv/bin
DB_FILE=humble_bundle.db
CMD_DOCKER=docker compose

etl:
	@$(VENV_BIN)/python -m spider.cli.run_spider

api:
	@$(VENV_BIN)/uvicorn api.main:app --reload --host 0.0.0.0 --port 5002

db-init:
	@echo "Inicializando base de datos SQLite..."
	@$(VENV_BIN)/python -c "from spider.database.session import get_session_factory; from spider.config.settings import get_settings; get_session_factory(get_settings())"
	@echo "Base de datos inicializada: $(DB_FILE)"

db-reset:
	@echo "Eliminando base de datos SQLite..."
	@rm -f $(DB_FILE)
	@echo "Base de datos eliminada. Ejecuta 'make db-init' para recrearla."

frontend-build:
	@cd frontend && npm run build

frontend-dev:
	@cd frontend && npm run dev

docker-up:
	@$(CMD_DOCKER) up -d

docker-down:
	@$(CMD_DOCKER) down -v

docker-restart:
	@$(CMD_DOCKER) down -v
	@$(CMD_DOCKER) up -d --build

help:
	@echo "Comandos disponibles:"
	@echo "  make etl              - Ejecutar ETL para descargar bundles"
	@echo "  make api              - Iniciar servidor API localmente"
	@echo "  make db-init          - Crear base de datos SQLite y tablas"
	@echo "  make db-reset         - Eliminar y recrear base de datos SQLite"
	@echo "  make frontend-build   - Ejecutar 'npm run build' en frontend/"
	@echo "  make frontend-dev     - Ejecutar 'npm run dev' en frontend/"
	@echo "  make docker-up        - Levantar docker compose en background"
	@echo "  make docker-down      - Detener y borrar volúmenes de docker compose"
	@echo "  make docker-restart   - Down + up --build para recrear contenedores"
