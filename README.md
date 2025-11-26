# Humble Scrape

ETL pipeline + API v1.0 + frontend to fetch public bundles from [Humble Bundle Books](https://www.humblebundle.com/books), normalize them and store them in SQLite.

## Main Stack
- Python 3.13 (3.12+ recommended)
- BeautifulSoup4 + Requests for scraping
- Pandas + Pydantic + Pydantic Settings for normalization and configuration
- SQLAlchemy 2 + SQLite (local development)
- FastAPI v1.0 + Uvicorn for the API
- Vue 3 + Vite + TypeScript for the interface

## Requirements
1. Python 3.12 or 3.13 with `venv` and updated `pip`.
2. Node.js 20+ (for the frontend).

## Backend Setup
```bash
git clone <repo>
cd humbleBundle
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
make db-init  # Inicializar base de datos SQLite
```

### Environment Variables (.env)
```env
DB_DB_PATH=humble_bundle.db
DB_SQL_ECHO=false
DB_JWT_SECRET_KEY=super-secret-key
DB_JWT_ACCESS_TOKEN_EXP_MINUTES=60
# Usuario inicial opcional (se crea/actualiza automáticamente si se define)
DB_ADMIN_USERNAME=admin
DB_ADMIN_EMAIL=admin@example.com
# Opción 1 (recomendada en desarrollo): contraseña en texto plano
DB_ADMIN_PASSWORD_PLAIN=supersecret
# Opción 2 (compatibilidad): SHA-256 hex de 64 chars
DB_ADMIN_PASSWORD_SHA=d2d2... (64 chars)
```

## Quick Makefile
- `make etl` – Run the ETL pipeline (uses `python -m spider.cli.run_spider`).
- `make api` – Start FastAPI with Uvicorn locally (http://0.0.0.0:5002).
- `make db-init` – Create SQLite database and tables.
- `make db-reset` – Delete and recreate SQLite database.
- `make frontend-dev` – Run frontend development server.
- `make frontend-build` – Build frontend for production.

## Run ETL via CLI
```bash
source .venv/bin/activate
python -m spider.cli.run_spider
# or
make etl
```
The command:
1. Fetches the JSON embedded in Humble Bundle's landing page.
2. Normalizes products with Pandas, enriches each bundle with individual details (price tiers, book list, MSRP, tile_logo) and validates with Pydantic.
3. Removes expired bundles and performs `upserts` in the `bundle` table in SQLite.

## FastAPI API v1.0
```bash
source .venv/bin/activate
uvicorn api.main:app --reload --host 0.0.0.0 --port 5002
# or
make api
```
Key endpoints:
- `GET /health`: service status.
- `GET /bundles`: complete list ordered by closing date.
- `GET /bundles/{bundle_id}`: details by UUID.
- `GET /bundles/by-machine-name/{machine_name}`: backward compatibility by `machine_name`.
- `GET /bundles/featured`: featured bundle according to total MSRP and sales.
- `POST /auth/login`: valida credenciales (`SHA-256` enviado desde frontend) y devuelve JWT.
- `GET /auth/me`: devuelve el usuario autenticado.
- `POST /etl/run`: triggers the spider, removes expired bundles and persists the result (requiere JWT Bearer).
- `GET /landing-page-raw-data`: list of raw data records.

**Note**: API v1.0 incluye el scraper original (HumbleSpider), protección básica por JWT para `/etl/run` y seed automático de un usuario admin si defines las variables `DB_ADMIN_*`.

### Seed automático de usuario
1. Define `DB_ADMIN_USERNAME`, `DB_ADMIN_EMAIL` y **alguna** de las variables de contraseña:
   - `DB_ADMIN_PASSWORD_PLAIN` (texto plano, el backend se encargará de hashear).
   - `DB_ADMIN_PASSWORD_SHA` (hash SHA-256 hex para compatibilidad u operaciones manuales).
2. Cada inicio de la API verificará/creará ese usuario y actualizará su e-mail o contraseña si cambias las variables.
3. Comandos útiles:
   - Crear/actualizar usuario sin levantar la API:
     ```bash
     python -m spider.cli.create_user \
       --username admin \
       --email admin@example.com \
       --password "<texto o sha256>"  # el backend lo normaliza automáticamente
     ```
   - Obtener el hash SHA-256 de una contraseña (opcional):
     ```bash
     python -m spider.cli.hash_password --password "mi-contraseña"
     ```

### Flujo de autenticación y hashing
1. El frontend envía la contraseña en texto plano usando HTTPS.
2. El backend normaliza todo como `bcrypt(SHA-256(plain))`.
3. Para obtener un token, envía `POST /auth/login` con `{ "username": "...", "password": "<texto>" }`.
4. Usa el token `Bearer` en las peticiones que lo requieran (`/etl/run`, `/auth/me`).

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

## Docker Compose
1. Copia `.env.example` a `.env` y ajusta los valores (`DB_*`, `DB_ADMIN_*`, `VITE_API_BASE_URL`, `FRONTEND_PORT`, etc.).
2. `docker-compose.yml` usa `env_file: .env` en todos los servicios, por lo que basta con mantener ese archivo en la raíz antes de ejecutar `docker compose up`.
3. El servicio `postgres` toma automáticamente `DB_PG*`, el backend `DB_*`/`DB_ADMIN_*`/`DB_JWT_*` y el frontend `VITE_API_BASE_URL` + `FRONTEND_PORT`.

## Repository Architecture
- `spider/`: ETL module.
  - `core/`: `HumbleSpider` class and custom exceptions.
  - `scrapers/`: fetches details for each bundle (tiers, books, tile_logo).
  - `database/`: SQLAlchemy `Bundle` model, sessions and persistence helpers (`persist_bundles`, `remove_outdated_bundles`).
  - `schemas/`: Pydantic models (`BundleRecord`).
  - `utils/`: transformations (text normalization, absolute URLs, metrics).
  - `config/`: settings based on Pydantic Settings (SQLite configuration).
  - `cli/`: entrypoint `run_spider.py`.
- `api/`: FastAPI v1.0 with sync/async dependencies and response schemas.
- `frontend/`: SPA in Vue 3 + Vite (responsive components, composables, custom typography).
- `docs/`: technical notes (`data_profile.md`, `frontend-style-stack.md`, `image-urls-pattern.md`).
- `Makefile`: main development automations (local development, no Docker).

## Database
The project uses SQLite for local development. The database file (`humble_bundle.db` by default) is created automatically when you run `make db-init` or when the API starts.

To reset the database:
```bash
make db-reset
```

## Suggested Next Steps
- Add unit/integration tests for spider, persistence and API.
- Extend frontend coverage (component and composable tests).
- Automate periodic ETL executions (cron, Celery or similar) and add basic authentication to the API.
- Generate historical snapshots in `docs/` and version the resulting datasets.
- If you change the model, recreate the database (`make db-reset`) before re-running the pipeline.
