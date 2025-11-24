.PHONY: etl api db-init db-reset frontend-build frontend-dev help

VENV_BIN=.venv/bin
DB_FILE=humble_bundle.db

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

help:
	@echo "Comandos disponibles:"
	@echo "  make etl              - Ejecutar ETL para descargar bundles"
	@echo "  make api              - Iniciar servidor API localmente"
	@echo "  make db-init          - Crear base de datos SQLite y tablas"
	@echo "  make db-reset         - Eliminar y recrear base de datos SQLite"
	@echo "  make frontend-build   - Ejecutar 'npm run build' en frontend/"
	@echo "  make frontend-dev     - Ejecutar 'npm run dev' en frontend/"
