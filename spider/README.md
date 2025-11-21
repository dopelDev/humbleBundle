# Spider de Humble Bundle

Este paquete encapsula el scraper ETL que obtiene bundles de **Humble Bundle Books**, normaliza los datos, descarga el detalle de cada bundle y persiste todo en PostgreSQL.

## Flujo general
- **`cli/run_spider.py`**: punto de entrada. Carga configuración (`DB_*`), ejecuta `HumbleSpider`, elimina bundles expirados y guarda los nuevos/actualizados.
- **`core/HumbleSpider`**: hace GET a `https://www.humblebundle.com/books`, lee el `<script id="landingPage-json-data">`, normaliza campos con pandas y Pydantic (`BundleRecord`), y para cada bundle consulta el detalle con `ImageUrlScraper`.
- **`scrapers/ImageUrlScraper`**: descarga la página del bundle (`webpack-bundle-page-data`), extrae tiers, libros, imagen destacada y todas las URLs de imágenes encontradas en el HTML (soup + regex).
- **Persistencia**: `database/persistence.py` hace upsert de los bundles (clave `machine_name`), recrea columnas faltantes, y guarda las URLs de imágenes scrapeadas asociadas al bundle.

## Explicación por archivo

### CLI
- `cli/run_spider.py`: script ejecutable. Orquesta el flujo completo: lee settings con `get_settings()`, instancia `HumbleSpider`, captura `HumbleSpiderError` para salir con código distinto de cero, borra bundles expirados con `remove_outdated_bundles` y persiste resultados con `persist_bundles`. Crea sesiones usando `get_session_factory`.

### Core
- `core/spider.py`: clase `HumbleSpider`.
  - Constantes `URL`, `SCRIPT_ID`, listas de columnas JSON/fecha/texto.
  - `fetch_bundles()`: pipeline principal: obtiene payload, extrae productos, normaliza DataFrame, convierte a `BundleRecord`.
  - `_fetch_raw_payload()`: hace GET al listado y parsea el script JSON embebido, levantando `HumbleSpiderError` si falta.
  - `_extract_products()`: navega el JSON `data.books.mosaic[0].products` y lanza excepción si la estructura cambia.
  - `_normalize_products()`: usa pandas para limpiar, convertir fechas a UTC, serializar campos JSON, normalizar texto, absolutizar URLs y calcular `duration_days`/`is_active`.
  - `_to_records()`: itera filas, pide detalle por bundle, fusiona `price_tiers`, `book_list`, `featured_image`, `msrp_total`, `raw_html` y URLs scrapeadas; valida con Pydantic y descarta registros inválidos con logging.
- `core/errors.py`: define excepciones de dominio `HumbleSpiderError` e `ImageUrlScraperError` (esta última hoy no se lanza desde `ImageUrlScraper`).

### Scrapers
- `scrapers/image_scraper.py`: clase `ImageUrlScraper`.
  - `fetch_detail(product_path, machine_name)`: descarga la página de un bundle, busca el `<script id="webpack-bundle-page-data">` para leer `bundleData`, arma tiers (`_extract_price_tiers`), libros (`_extract_book_list`), msrp total, imagen destacada y guarda `raw_html`.
  - `_extract_jpg_urls_from_html_with_info()`: recorre HTML con BeautifulSoup + regex para recopilar todas las URLs de imágenes (absolutas) con metadatos de fuente (`img_tag`, `style`, `data_attr`, `json`, `regex`) y mantiene un mapeo filename→URL para resolver rutas relativas del JSON.
  - `_resolve_image_url()`: intenta resolver una URL parcial (del JSON) contra el mapeo de URLs encontradas; como fallback, construye URL absoluta con `BASE_URL`.
  - Helpers: normalización de URLs relativas a absolutas, extracción de URLs desde JSON arbitrario, parseo de filename desde URL. Incluye dataclass `BundleDetail` y `ScrapedImageUrlInfo`.

### Schemas
- `schemas/bundle.py`: modelo Pydantic `BundleRecord`.
  - Define todos los campos del bundle con aliases (ej. `start_date|datetime`), longitudes máximas y tipos (`HttpUrl`, `datetime`, `float`).
  - Validadores: convierten highlights a string, controlan no negativos en `bundles_sold_decimal`/`duration_days`.
  - `to_orm_payload()`: adapta el diccionario para la capa ORM (cambia `type`→`_type`, cast de URL a string).

### Base de datos
- `database/models.py`: modelos SQLAlchemy.
  - `Bundle`: tabla principal con metadatos del bundle, tiers/libros en JSON, imagen destacada, HTML crudo, flags y relaciones a `ImageURL`/`ScrapedImageURL`.
  - `ScrapedImageURL`: guarda cada URL absoluta encontrada en el HTML de un bundle con info de fuente/atributo y fecha de scraping.
  - `ImageURL`: almacena URLs originales y real_path resueltas para imágenes (featured/book), con tipo de match y fecha de verificación.
- `database/session.py`: fábrica de sesión.
  - Construye URI con settings, crea la BD si no existe, verifica existencia de `bundle` vía SQL simple, usa `Base.metadata.create_all(checkfirst=True)` como fallback.
  - Llama a `ensure_columns`, `ensure_image_url_table`, `ensure_scraped_image_url_table` para mantener el esquema mínimo.
- `database/persistence.py`: operaciones de persistencia y mantenimiento.
  - `persist_bundles`: upsert (ON CONFLICT machine_name) de bundles; luego limpia e inserta URLs scrapeadas (`ScrapedImageURL`) asociadas a los bundles recién cargados.
  - `remove_outdated_bundles`: borra bundles con `end_date_datetime` en el pasado.
  - `recreate_database`: recrea la base opcionalmente borrando la existente; crea tablas y columnas auxiliares.
  - `ensure_columns/ensure_image_url_table/ensure_scraped_image_url_table`: migraciones rápidas en SQL crudo para añadir columnas/tablas si faltan.

### Configuración
- `config/settings.py`: clase `Settings` (pydantic-settings) con prefijo `DB_` y `.env` opcional; contiene credenciales y `sql_echo`.

### Utilidades
- `utils/transformers.py`: helpers comunes.
  - `normalize_text`, `serialize_list`, `absolute_url`, `safe_float`.
  - Cálculo de `compute_duration_days` e `is_active` contra fechas UTC.
  - `normalize_columns` aplica `normalize_text` a columnas pandas especificadas.
- `utils/__init__.py`: exporta helpers.

### Paquete raíz
- `spider/__init__.py`: exporta clases/funciones principales para import fácil (`HumbleSpider`, modelos, schemas, settings, helpers de persistencia).

## Esquema de datos (PostgreSQL)
- **bundle**: datos normalizados del listado + detalles (tiers, libros, imagen destacada, HTML raw, flags `is_active`/`duration_days`).
- **scraped_image_url**: todas las URLs absolutas de imágenes encontradas en el HTML de cada bundle, con origen (`img_tag`, `style`, `data_attr`, `json`, `regex`).
- **image_url**: URLs originales y “real paths” resueltos para imágenes destacadas y de libros, con tipo de match; se mantiene para análisis/validación posterior.

## Ejecución local
1) Exporta variables o `.env` con `DB_USER`, `DB_PASSWORD`, `DB_DATABASE`, `DB_HOST`, `DB_PORT` (valores por defecto: postgres/postgres/test/localhost/5432).
2) Ejecuta:
```bash
python -m spider.cli.run_spider
```
El flujo recreará tablas faltantes, borrará bundles expirados y hará upsert de los actuales.

## Consideraciones y limitaciones
- Depende de la estructura actual de la página: `<script id="landingPage-json-data">` para el listado y `<script id="webpack-bundle-page-data">` en cada bundle. Cambios en el sitio pueden romper el parseo.
- El detalle se descarga por bundle de forma secuencial; fallos de red devuelven `None` para ese bundle y se pierden `price_tiers/book_list/featured_image`.
- Solo se persisten registros que pasan validación Pydantic (fechas válidas); bundles sin fechas válidas se descartan.
- Las migraciones de esquema se realizan con SQL crudo simple (`ensure_*`); no hay sistema de migraciones formal.

## Próximos pasos recomendados
- Añadir reintentos/backoff/paralelización al fetch de detalle.
- Incluir pruebas con fixtures de HTML/JSON reales para detectar cambios de estructura.
- Migrar a un sistema de migraciones (Alembic) en lugar de SQL adhoc.
