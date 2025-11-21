# Humble Scrape

Pipeline ETL + API + frontend para obtener los bundles públicos de [Humble Bundle Books](https://www.humblebundle.com/books), normalizarlos y almacenarlos en PostgreSQL.

## Stack principal
- Python 3.13 (recomendado 3.12+)
- BeautifulSoup4 + Requests para scraping
- Pandas + Pydantic + Pydantic Settings para normalización y configuración
- SQLAlchemy 2 + PostgreSQL/asyncpg
- FastAPI + Uvicorn para la API
- Vue 3 + Vite + TypeScript para la interfaz

## Requisitos
1. PostgreSQL accesible (`postgres:postgres@localhost:5432/test` por defecto).
2. Python 3.12 o 3.13 con `venv` y `pip` actualizado.
3. Node.js 20+ (para el frontend).
4. (Opcional) Docker + Docker Compose para levantar Postgres + API.

## Configuración backend
```bash
git clone <repo>
cd humbleBundle
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Variables de entorno (.env)
```env
DB_PGUSER=postgres
DB_PGPASSWORD=postgres
DB_PGDATABASE=test
DB_PGHOST=localhost
DB_PGPORT=5432
DB_SQL_ECHO=false
```

## Makefile rápido
- `make etl` – Ejecutar el pipeline ETL (usa `python -m spider.cli.run_spider`).
- `make api` – Levantar FastAPI con Uvicorn usando el entorno virtual.
- `make compose-up` / `make compose-down` – Levantar o apagar los servicios declarados en `docker-compose.dev.yml`.
- `make recreate-db` – Dropear y recrear todas las tablas.
- `make recreate-volumes` – Borrar volúmenes Docker (`pgdata`, `images`).
- `make clean-network` – Limpiar redes huérfanas creadas por Compose.

## Ejecutar el ETL por CLI
```bash
source .venv/bin/activate
python -m spider.cli.run_spider
# o
make etl
```
El comando:
1. Obtiene el JSON embebido en la landing de Humble Bundle.
2. Normaliza los productos con Pandas, enriquece cada bundle con detalle individual (tiers de precio, lista de libros, MSRP, featured image) y valida con Pydantic.
3. Elimina bundles expirados y hace `upserts` en la tabla `bundle`, registrando también las URLs de imágenes encontradas.

## API FastAPI
```bash
source .venv/bin/activate
uvicorn api.main:app --reload
# o
make api
```
Endpoints clave:
- `GET /health`: estado del servicio.
- `GET /bundles`: listado completo ordenado por fecha de cierre.
- `GET /bundles/{bundle_id}`: detalle por UUID.
- `GET /bundles/by-machine-name/{machine_name}`: retrocompatibilidad por `machine_name`.
- `GET /bundles/featured`: bundle destacado según MSRP total y ventas.
- `POST /etl/run`: dispara el spider, elimina bundles expirados y persiste el resultado.

La API monta `/images` para servir archivos estáticos desde `images/bundles` e `images/books`, útil al desplegar con Docker.

## Docker Compose (dev)
`docker-compose.dev.yml` incluye:
- PostgreSQL 16 + volumen `pgdata`.
- Servicio `api` basado en `python:3.11` que instala `requirements.txt` y expone FastAPI en `0.0.0.0:5002`.

```bash
docker compose -f docker-compose.dev.yml up -d
# o
make compose-up
```

## Frontend (Vue + Vite)
La carpeta `frontend/` contiene una SPA que replica el look & feel del sitio original y consume la API.
```bash
cd frontend
npm install
npm run dev # http://localhost:3002
```
Variables disponibles:
```bash
VITE_API_BASE_URL=http://127.0.0.1:5002
```
Consulta `frontend/README.md` para scripts (`build`, `preview`), temas claro/oscuro y estructura de componentes.

## Arquitectura del repositorio
- `spider/`: módulo ETL.
  - `core/`: clase `HumbleSpider` y excepciones custom.
  - `scrapers/`: obtiene detalles de cada bundle (tiers, libros, imágenes).
  - `database/`: modelos SQLAlchemy (`Bundle`, `ImageURL`, `ScrapedImageURL`), sesiones y helpers de persistencia (`persist_bundles`, `remove_outdated_bundles`, `recreate_database`).
  - `schemas/`: modelos Pydantic (`BundleRecord`).
  - `utils/`: transformaciones (normalización de texto, URLs absolutas, métricas).
  - `config/`: settings basados en Pydantic Settings.
  - `cli/`: entrypoint `run_spider.py`.
- `api/`: FastAPI con dependencias sync/async, schemas de respuesta y montaje de `/images`.
- `scripts/`: utilidades CLI como `recreate_db.py`.
- `frontend/`: SPA en Vue 3 + Vite (componentes responsive, composables, tipografías custom).
- `docs/`: notas técnicas (`data_profile.md`, `frontend-style-stack.md`, `image-urls-pattern.md`).
- `images/`: buckets locales (`images/bundles`, `images/books`) que también se montan como volumen en Docker.
- `Makefile` y `docker-compose.dev.yml`: automatizaciones principales para desarrollo.

## Próximos pasos sugeridos
- Añadir pruebas unitarias/integración para spider, persistencia y API.
- Extender la cobertura del frontend (tests de componentes y composables).
- Automatizar ejecuciones periódicas del ETL (cron, Celery o similar) y añadir autenticación básica en la API.
- Generar snapshots históricos en `docs/` y versionar los datasets resultantes.
- Si cambias el modelo, recrea la base (`make recreate-db`) o los volúmenes Docker antes de reejecutar el pipeline.
