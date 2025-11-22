# Spider de Humble Bundle

Este paquete encapsula el scraper ETL que obtiene bundles de **Humble Bundle Books**, normaliza los datos, descarga el detalle de cada bundle y persiste todo en PostgreSQL.

## Estructura del Módulo

```
spider/
├── __init__.py              # Exporta clases/funciones principales
├── README.md                # Este archivo
│
├── cli/                     # Punto de entrada CLI
│   ├── __init__.py
│   └── run_spider.py        # Script ejecutable principal
│
├── core/                    # Lógica principal del spider
│   ├── __init__.py
│   ├── errors.py            # Excepciones personalizadas
│   └── spider.py            # Clase HumbleSpider
│
├── scrapers/                # Scrapers especializados
│   ├── __init__.py
│   └── image_scraper.py     # ImageUrlScraper (detalles de bundles)
│
├── schemas/                 # Modelos Pydantic
│   ├── __init__.py
│   └── bundle.py            # BundleRecord
│
├── database/                # Capa de persistencia
│   ├── __init__.py
│   ├── models.py            # Modelos SQLAlchemy (Bundle, LandingPageRawData)
│   ├── persistence.py       # Funciones de persistencia (persist_bundles, etc.)
│   └── session.py           # Fábrica de sesiones SQLAlchemy
│
├── config/                  # Configuración
│   ├── __init__.py
│   └── settings.py          # Settings (Pydantic Settings)
│
└── utils/                   # Utilidades y transformadores
    ├── __init__.py
    └── transformers.py      # Funciones de normalización y transformación
```

## Arquitectura General

El sistema implementa un pipeline ETL (Extract, Transform, Load) para obtener, normalizar y persistir bundles de Humble Bundle Books. La arquitectura se organiza en capas bien definidas:

1. **Extracción**: Obtiene datos del sitio web mediante scraping
2. **Transformación**: Normaliza y enriquece los datos
3. **Carga**: Persiste los datos en PostgreSQL

### Componentes Principales

- **CLI** (`cli/run_spider.py`): Punto de entrada que orquesta el flujo completo
- **Core** (`core/spider.py`): Clase `HumbleSpider` que maneja la extracción y transformación
- **Scrapers** (`scrapers/image_scraper.py`): Enriquecimiento de datos con detalles de cada bundle
- **Schemas** (`schemas/`): Validación de datos con Pydantic (`BundleRecord`, `LandingPageRawDataRecord`)
- **Database** (`database/`): Modelos ORM, persistencia y gestión de sesiones
- **Config** (`config/settings.py`): Configuración basada en variables de entorno
- **Utils** (`utils/transformers.py`): Funciones auxiliares de transformación

## Flujo general

- **`cli/run_spider.py`**: punto de entrada. Carga configuración (`DB_*`), ejecuta `HumbleSpider`, elimina bundles expirados y guarda los nuevos/actualizados.
- **`core/HumbleSpider`**: hace GET a `https://www.humblebundle.com/books`, lee el `<script id="landingPage-json-data">`, normaliza campos con pandas y Pydantic (`BundleRecord`), y para cada bundle consulta el detalle con `ImageUrlScraper`.
- **`scrapers/ImageUrlScraper`**: descarga la página del bundle (`webpack-bundle-page-data`), extrae tiers, libros, imagen destacada y todas las URLs de imágenes encontradas en el HTML (soup + regex).
- **Persistencia**: `database/persistence.py` hace upsert de los bundles (clave `machine_name`), recrea columnas faltantes y permite archivar el JSON bruto de `landingPage-json-data`.

## Modelo de Datos

### Tabla bundle

```
┌─────────────────────────────────────────────────────────────────┐
│                          BUNDLE                                 │
├─────────────────────────────────────────────────────────────────┤
│ PK  id                          UUID                            │
│ UNQ machine_name               VARCHAR(255)  NOT NULL           │
│     high_res_tile_image         VARCHAR(2048)                   │
│     disable_hero_tile           BOOLEAN                         │
│     marketing_blurb             VARCHAR(1024)                   │
│     hover_title                 VARCHAR(255)                    │
│     product_url                 VARCHAR                          │
│     tile_image                  VARCHAR(2048)                   │
│     category                    VARCHAR(128)                    │
│     hero_highlights             VARCHAR                         │
│     hover_highlights            VARCHAR                         │
│     author                      VARCHAR(255)                    │
│     supports_partners           BOOLEAN                         │
│     detailed_marketing_blurb    VARCHAR(2048)                   │
│     tile_logo                   VARCHAR(2048)                   │
│     tile_short_name             VARCHAR(255)                    │
│     start_date_datetime         TIMESTAMP  (INDEX)              │
│     end_date_datetime           TIMESTAMP  (INDEX)              │
│     tile_stamp                  VARCHAR(64)                     │
│     bundles_sold_decimal        FLOAT                           │
│     tile_name                   VARCHAR(255)                    │
│     short_marketing_blurb       VARCHAR(512)                    │
│     _type                       VARCHAR                         │
│     highlights                  VARCHAR                         │
│     tile_logo_information_*     VARCHAR                         │
│     high_res_tile_image_info_*  VARCHAR                         │
│     tile_image_information_*    VARCHAR                         │
│     verification_date           TIMESTAMP  NOT NULL             │
│     duration_days               FLOAT                           │
│     is_active                   BOOLEAN  (INDEX)                │
│     price_tiers                 JSONB                           │
│     book_list                   JSONB                           │
│     featured_image              VARCHAR                         │
│     msrp_total                  FLOAT                           │
│     raw_html                    TEXT                            │
└─────────────────────────────────────────────────────────────────┘
```

### Tabla landing_page_raw_data

```
┌────────────────────────────────────────────────┐
│             LANDING_PAGE_RAW_DATA              │
├────────────────────────────────────────────────┤
│ PK  id              UUID                       │
│     json_data       JSONB      NOT NULL        │
│     scraped_date    TIMESTAMP  (INDEX)         │
│     source_url      VARCHAR    NOT NULL        │
│     json_hash       VARCHAR    (INDEX)         │
│     json_version    VARCHAR                    │
└────────────────────────────────────────────────┘
```

La tabla `bundle` almacena los metadatos enriquecidos de cada bundle, y `landing_page_raw_data` guarda el JSON bruto del script `landingPage-json-data` con su metadata (fecha, hash, versión) para trazabilidad y auditoría.

## Flujo de Datos Completo

```
┌─────────────────────────────────────────────────────────────────────┐
│                        1. EXTRACCIÓN                                │
├─────────────────────────────────────────────────────────────────────┤
│ HumbleSpider.fetch_bundles()                                        │
│   └─> GET https://www.humblebundle.com/books                        │
│       └─> Extrae <script id="landingPage-json-data">               │
│           └─> Parsea JSON → products[]                              │
└─────────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      2. TRANSFORMACIÓN                              │
├─────────────────────────────────────────────────────────────────────┤
│ HumbleSpider._normalize_products()                                  │
│   └─> pandas.json_normalize()                                       │
│       ├─> Convierte fechas a UTC                                    │
│       ├─> Serializa campos JSON                                     │
│       ├─> Normaliza texto (trim, nulls)                             │
│       ├─> Absolutiza URLs                                           │
│       └─> Calcula duration_days, is_active                          │
└─────────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      3. ENRIQUECIMIENTO                             │
├─────────────────────────────────────────────────────────────────────┤
│ HumbleSpider._to_records()                                          │
│   Para cada producto:                                               │
│     └─> ImageUrlScraper.fetch_detail(product_url)                   │
│         ├─> GET página del bundle                                   │
│         ├─> Extrae <script id="webpack-bundle-page-data">          │
│         ├─> Extrae URLs de imágenes del HTML:                       │
│         │   ├─> <img> tags (src, data-src, srcset)                  │
│         │   ├─> style="background-image: url(...)"                  │
│         │   ├─> data-image, data-bg attributes                      │
│         │   ├─> JSON embebido                                       │
│         │   └─> Regex para .jpg/.jpeg                               │
│         ├─> Resuelve URLs relativas → absolutas                     │
│         ├─> Extrae price_tiers, book_list, featured_image          │
│         └─> Guarda raw_html                                         │
└─────────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        4. VALIDACIÓN                                │
├─────────────────────────────────────────────────────────────────────┤
│ BundleRecord.model_validate(item)                                   │
│   └─> Pydantic valida tipos, longitudes, formatos                   │
│       └─> Registros inválidos → descartados (log)                   │
└─────────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                          5. PERSISTENCIA                            │
├─────────────────────────────────────────────────────────────────────┤
│ persist_bundles(records, session)                                   │
│   ├─> UPSERT en tabla 'bundle' (ON CONFLICT machine_name)          │
│   │   └─> Actualiza todos los campos excepto 'id'                   │
│                                                                      │
│ remove_outdated_bundles(session)                                    │
│   └─> DELETE bundles donde end_date_datetime < NOW()               │
└─────────────────────────────────────────────────────────────────────┘
```

### Índices Principales

- `bundle.id` (PRIMARY KEY)
- `bundle.machine_name` (UNIQUE, INDEX)
- `bundle.start_date_datetime` (INDEX)
- `bundle.end_date_datetime` (INDEX)
- `bundle.is_active` (INDEX)
- `landing_page_raw_data.scraped_date` (INDEX)
- `landing_page_raw_data.json_hash` (INDEX)

## Explicación por archivo

### CLI

- `cli/run_spider.py`: script ejecutable. Orquesta el flujo completo: lee settings con `get_settings()`, instancia `HumbleSpider`, captura `HumbleSpiderError` para salir con código distinto de cero, borra bundles expirados con `remove_outdated_bundles` y persiste resultados con `persist_bundles`. Crea sesiones usando `get_session_factory`.

### Core

- `core/spider.py`: clase `HumbleSpider`.
  - Constantes `URL`, `SCRIPT_ID`, listas de columnas JSON/fecha/texto.
  - `fetch_bundles()`: pipeline principal: obtiene payload, extrae productos, normaliza DataFrame, convierte a `BundleRecord`.
  - `get_raw_data_record()`: expone el último JSON bruto (`landingPage-json-data`) con hash y metadata listo para persistir en `landing_page_raw_data`.
  - `_fetch_raw_payload()`: hace GET al listado y parsea el script JSON embebido, levantando `HumbleSpiderError` si falta.
  - `_extract_products()`: navega el JSON `data.books.mosaic[0].products` y lanza excepción si la estructura cambia.
  - `_normalize_products()`: usa pandas para limpiar, convertir fechas a UTC, serializar campos JSON, normalizar texto, absolutizar URLs y calcular `duration_days`/`is_active`.
  - `_to_records()`: itera filas, pide detalle por bundle, fusiona `price_tiers`, `book_list`, `featured_image`, `msrp_total` y `raw_html`; valida con Pydantic y descarta registros inválidos con logging.
- `core/errors.py`: define excepciones de dominio `HumbleSpiderError` e `ImageUrlScraperError` (esta última hoy no se lanza desde `ImageUrlScraper`).

### Scrapers

- `scrapers/image_scraper.py`: clase `ImageUrlScraper`.
  - `fetch_detail(product_path, machine_name)`: descarga la página de un bundle, busca el `<script id="webpack-bundle-page-data">` para leer `bundleData`, arma tiers (`_extract_price_tiers`), libros (`_extract_book_list`), msrp total, imagen destacada y guarda `raw_html`.
  - `_extract_jpg_urls_from_html_with_info()`: recorre HTML con BeautifulSoup + regex para recopilar URLs de imágenes absolutas y mantener un mapeo filename→URL que ayuda a resolver rutas relativas del JSON.
  - `_resolve_image_url()`: intenta resolver una URL parcial (del JSON) contra el mapeo de URLs encontradas; como fallback, construye URL absoluta con `BASE_URL`.
  - Helpers: normalización de URLs relativas a absolutas, extracción de URLs desde JSON arbitrario, parseo de filename desde URL. Incluye dataclass `BundleDetail`.

### Schemas

- `schemas/bundle.py`: modelo Pydantic `BundleRecord`.
  - Define todos los campos del bundle con aliases (ej. `start_date|datetime`), longitudes máximas y tipos (`HttpUrl`, `datetime`, `float`).
  - Validadores: convierten highlights a string, controlan no negativos en `bundles_sold_decimal`/`duration_days`.
  - `to_orm_payload()`: adapta el diccionario para la capa ORM (cambia `type`→`_type`, cast de URL a string).
- `schemas/raw_data.py`: modelo Pydantic `LandingPageRawDataRecord`.
  - Guarda el JSON bruto del script `landingPage-json-data` con `scraped_date`, `source_url`, hash (`json_hash`) y campo de versión opcional.
  - `to_orm_payload()`: devuelve el diccionario listo para persistir en `landing_page_raw_data`.

### Base de datos

- `database/models.py`: modelos SQLAlchemy.
  - `Bundle`: tabla principal con metadatos del bundle, tiers/libros en JSON, imagen destacada y HTML crudo.
  - `LandingPageRawData`: almacena el JSON bruto del script `landingPage-json-data` con hash y metadata de scraping.
- `database/session.py`: fábrica de sesión.
  - Construye URI con settings, crea la BD si no existe, verifica existencia de `bundle` vía SQL simple, usa `Base.metadata.create_all(checkfirst=True)` como fallback.
  - Llama a `ensure_columns` y `ensure_landing_page_raw_data_table` para mantener el esquema mínimo.
- `database/persistence.py`: operaciones de persistencia y mantenimiento.
  - `persist_bundles`: upsert (ON CONFLICT machine_name) de bundles.
  - `persist_landing_page_raw_data`: inserta el JSON bruto de landingPage con metadata.
  - `remove_outdated_bundles`: borra bundles con `end_date_datetime` en el pasado.
  - `recreate_database`: recrea la base opcionalmente borrando la existente; crea tablas y columnas auxiliares.
  - `ensure_columns` y `ensure_landing_page_raw_data_table`: migraciones rápidas en SQL crudo para añadir columnas/tablas si faltan.

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
- **landing_page_raw_data**: snapshots del JSON bruto de `landingPage-json-data` con fecha de scraping, URL fuente, hash y versión opcional.

## Ejecución local

1. Exporta variables o `.env` con `DB_USER`, `DB_PASSWORD`, `DB_DATABASE`, `DB_HOST`, `DB_PORT` (valores por defecto: postgres/postgres/test/localhost/5432).
2. Ejecuta:

```bash
python -m spider.cli.run_spider
```

El flujo recreará tablas faltantes, borrará bundles expirados y hará upsert de los actuales.

El JSON bruto (`landingPage-json-data`) de la fase de extracción puede almacenarse en `landing_page_raw_data` combinando `HumbleSpider.get_raw_data_record()` con `persist_landing_page_raw_data()`.

## Consideraciones y limitaciones

- Depende de la estructura actual de la página: `<script id="landingPage-json-data">` para el listado y `<script id="webpack-bundle-page-data">` en cada bundle. Cambios en el sitio pueden romper el parseo.
- El detalle se descarga por bundle de forma secuencial; fallos de red devuelven `None` para ese bundle y se pierden `price_tiers/book_list/featured_image`.
- Solo se persisten registros que pasan validación Pydantic (fechas válidas); bundles sin fechas válidas se descartan.
- Las migraciones de esquema se realizan con SQL crudo simple (`ensure_*`); no hay sistema de migraciones formal.

## Resumen de Características

### Ventajas del Sistema

1. **Arquitectura ETL Clara**: Separación bien definida entre extracción, transformación y carga
2. **Normalización Robusta**: Uso de pandas para limpieza y Pydantic para validación estricta
3. **Enriquecimiento de Datos**: Scraping detallado de cada bundle con resolución inteligente de URLs de imágenes
4. **Persistencia Eficiente**: UPSERT con ON CONFLICT para actualizar sin duplicados
5. **Trazabilidad**: Almacenamiento de HTML raw y snapshots del `landingPage-json-data` con hash para análisis posterior
6. **Configuración Flexible**: Settings basados en variables de entorno con valores por defecto sensatos
7. **Manejo de Errores**: Excepciones específicas del dominio y logging detallado

### Funcionalidades Clave

- **Scraping de URLs de Imágenes**: Extracción multi-fuente (img tags, styles, data-attributes, JSON, regex)
- **Resolución de URLs**: Mapeo inteligente de URLs relativas a absolutas usando el HTML del bundle
- **Normalización de Datos**: Limpieza de texto, conversión de fechas, serialización JSON
- **Validación Estricta**: Validación Pydantic con descarte de registros inválidos
- **Mantenimiento Automático**: Limpieza de bundles expirados y actualización de columnas faltantes

## Próximos pasos recomendados

- Añadir reintentos/backoff/paralelización al fetch de detalle.
- Incluir pruebas con fixtures de HTML/JSON reales para detectar cambios de estructura.
- Migrar a un sistema de migraciones (Alembic) en lugar de SQL adhoc.
