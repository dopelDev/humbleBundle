# Humble Scrape

ETL pipeline + API + frontend to fetch public bundles from [Humble Bundle Books](https://www.humblebundle.com/books), normalize them and store them in PostgreSQL.

## Main Stack
- Python 3.13 (3.12+ recommended)
- BeautifulSoup4 + Requests for scraping
- Pandas + Pydantic + Pydantic Settings for normalization and configuration
- SQLAlchemy 2 + PostgreSQL/asyncpg
- FastAPI + Uvicorn for the API
- Vue 3 + Vite + TypeScript for the interface

## Requirements
1. Accessible PostgreSQL (`postgres:postgres@localhost:5432/test` by default).
2. Python 3.12 or 3.13 with `venv` and updated `pip`.
3. Node.js 20+ (for the frontend).
4. (Optional) Docker + Docker Compose to run Postgres + API.

## Backend Setup
```bash
git clone <repo>
cd humbleBundle
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Environment Variables (.env)
```env
DB_PGUSER=postgres
DB_PGPASSWORD=postgres
DB_PGDATABASE=test
DB_PGHOST=localhost
DB_PGPORT=5432
DB_SQL_ECHO=false
```

## Quick Makefile
- `make etl` – Run the ETL pipeline (uses `python -m spider.cli.run_spider`).
- `make api` – Start FastAPI with Uvicorn using the virtual environment.
- `make compose-up` / `make compose-down` – Start or stop services declared in `docker-compose.dev.yml`.
- `make recreate-db` – Drop and recreate all tables.
- `make recreate-volumes` – Delete Docker volumes (`pgdata`, `images`).
- `make clean-network` – Clean orphaned networks created by Compose.

## Run ETL via CLI
```bash
source .venv/bin/activate
python -m spider.cli.run_spider
# or
make etl
```
The command:
1. Fetches the JSON embedded in Humble Bundle's landing page.
2. Normalizes products with Pandas, enriches each bundle with individual details (price tiers, book list, MSRP, featured image) and validates with Pydantic.
3. Removes expired bundles and performs `upserts` in the `bundle` table, also recording the image URLs found.

## FastAPI API
```bash
source .venv/bin/activate
uvicorn api.main:app --reload
# or
make api
```
Key endpoints:
- `GET /health`: service status.
- `GET /bundles`: complete list ordered by closing date.
- `GET /bundles/{bundle_id}`: details by UUID.
- `GET /bundles/by-machine-name/{machine_name}`: backward compatibility by `machine_name`.
- `GET /bundles/featured`: featured bundle according to total MSRP and sales.
- `POST /etl/run`: triggers the spider, removes expired bundles and persists the result.

The API mounts `/images` to serve static files from `images/bundles` and `images/books`, useful when deploying with Docker.

## Docker Compose (dev)
`docker-compose.dev.yml` includes:
- PostgreSQL 16 + `pgdata` volume.
- `api` service based on `python:3.11` that installs `requirements.txt` and exposes FastAPI on `0.0.0.0:5002`.

```bash
docker compose -f docker-compose.dev.yml up -d
# or
make compose-up
```

## Frontend (Vue + Vite)
The `frontend/` folder contains a SPA that replicates the original site's look & feel and consumes the API.
```bash
cd frontend
npm install
npm run dev # http://localhost:3002
```
Available variables:
```bash
VITE_API_BASE_URL=http://127.0.0.1:5002
```
See `frontend/README.md` for scripts (`build`, `preview`), light/dark themes and component structure.

## Repository Architecture
- `spider/`: ETL module.
  - `core/`: `HumbleSpider` class and custom exceptions.
  - `scrapers/`: fetches details for each bundle (tiers, books, images).
  - `database/`: SQLAlchemy `Bundle` model, sessions and persistence helpers (`persist_bundles`, `remove_outdated_bundles`, `recreate_database`).
  - `schemas/`: Pydantic models (`BundleRecord`).
  - `utils/`: transformations (text normalization, absolute URLs, metrics).
  - `config/`: settings based on Pydantic Settings.
  - `cli/`: entrypoint `run_spider.py`.
- `api/`: FastAPI with sync/async dependencies, response schemas and `/images` mounting.
- `scripts/`: CLI utilities like `recreate_db.py`.
- `frontend/`: SPA in Vue 3 + Vite (responsive components, composables, custom typography).
- `docs/`: technical notes (`data_profile.md`, `frontend-style-stack.md`, `image-urls-pattern.md`).
- `images/`: local buckets (`images/bundles`, `images/books`) that are also mounted as volumes in Docker.
- `Makefile` and `docker-compose.dev.yml`: main development automations.

## Suggested Next Steps
- Add unit/integration tests for spider, persistence and API.
- Extend frontend coverage (component and composable tests).
- Automate periodic ETL executions (cron, Celery or similar) and add basic authentication to the API.
- Generate historical snapshots in `docs/` and version the resulting datasets.
- If you change the model, recreate the database (`make recreate-db`) or Docker volumes before re-running the pipeline.
