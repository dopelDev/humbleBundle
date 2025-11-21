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
│   ├── models.py            # Modelos SQLAlchemy (Bundle, ScrapedImageURL, ImageURL)
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
- **Schemas** (`schemas/bundle.py`): Validación de datos con Pydantic
- **Database** (`database/`): Modelos ORM, persistencia y gestión de sesiones
- **Config** (`config/settings.py`): Configuración basada en variables de entorno
- **Utils** (`utils/transformers.py`): Funciones auxiliares de transformación

## Flujo general
- **`cli/run_spider.py`**: punto de entrada. Carga configuración (`DB_*`), ejecuta `HumbleSpider`, elimina bundles expirados y guarda los nuevos/actualizados.
- **`core/HumbleSpider`**: hace GET a `https://www.humblebundle.com/books`, lee el `<script id="landingPage-json-data">`, normaliza campos con pandas y Pydantic (`BundleRecord`), y para cada bundle consulta el detalle con `ImageUrlScraper`.
- **`scrapers/ImageUrlScraper`**: descarga la página del bundle (`webpack-bundle-page-data`), extrae tiers, libros, imagen destacada y todas las URLs de imágenes encontradas en el HTML (soup + regex).
- **Persistencia**: `database/persistence.py` hace upsert de los bundles (clave `machine_name`), recrea columnas faltantes, y guarda las URLs de imágenes scrapeadas asociadas al bundle.

## Diagrama ER (Modelo de Datos)

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
                              │
                              │ 1:N
                              │ (CASCADE DELETE)
                              ├──────────────────────────────┐
                              │                              │
                              ▼                              ▼
┌──────────────────────────────────┐    ┌──────────────────────────────────┐
│     SCRAPED_IMAGE_URL            │    │         IMAGE_URL                │
├──────────────────────────────────┤    ├──────────────────────────────────┤
│ PK  id                  UUID     │    │ PK  id                  UUID     │
│ FK  bundle_id           UUID     │    │ FK  bundle_id           UUID     │
│     url                 VARCHAR  │    │     image_type          VARCHAR  │
│     source              VARCHAR  │    │     book_machine_name   VARCHAR  │
│     attribute           VARCHAR  │    │     original_url        VARCHAR  │
│     scraped_date        TIMESTAMP│    │     real_path           VARCHAR  │
│                              │    │     match_type            VARCHAR  │
│                              │    │     verification_date      TIMESTAMP│
└──────────────────────────────┘    └──────────────────────────────────┘
```

### Relaciones

- **Bundle (1) ──< (N) ScrapedImageURL**: Un bundle tiene muchas URLs scrapeadas. Borrado en cascada.
- **Bundle (1) ──< (N) ImageURL**: Un bundle tiene muchas URLs de imágenes. Borrado en cascada.

### Descripción de Entidades

#### Bundle (Entidad Principal)
- **Propósito**: Almacena todos los metadatos de un bundle de Humble Bundle
- **Clave Primaria**: `id` (UUID generado automáticamente)
- **Clave Única**: `machine_name` (identificador único del bundle)
- **Campos Importantes**:
  - `machine_name`: Identificador único del bundle (indexado)
  - `start_date_datetime`, `end_date_datetime`: Fechas de inicio y fin del bundle (indexadas)
  - `is_active`: Bandera calculada según las fechas (indexada)
  - `price_tiers`, `book_list`: Datos estructurados en formato JSONB
  - `raw_html`: HTML completo del bundle para tests y análisis
  - `verification_date`: Timestamp de cuando se verificó/actualizó el bundle

#### ScrapedImageURL
- **Propósito**: Almacena todas las URLs absolutas de imágenes encontradas en el HTML del bundle
- **Clave Primaria**: `id` (UUID)
- **Clave Foránea**: `bundle_id` → `Bundle.id` (CASCADE DELETE)
- **Campos**:
  - `url`: URL absoluta de la imagen (imgix, CDN, etc.)
  - `source`: Origen de la URL (`img_tag`, `style`, `data_attr`, `json`, `regex`)
  - `attribute`: Atributo específico si aplica (`src`, `data-src`, `background-image`, etc.)
  - `scraped_date`: Fecha de scraping (indexada)

#### ImageURL
- **Propósito**: Almacena URLs de imágenes específicas (featured o de libros) con su URL original y la real resuelta
- **Clave Primaria**: `id` (UUID)
- **Clave Foránea**: `bundle_id` → `Bundle.id` (CASCADE DELETE)
- **Campos**:
  - `image_type`: Tipo de imagen (`featured_image` o `book_image`)
  - `book_machine_name`: Machine name del libro (solo para `book_image`)
  - `original_url`: URL original del JSON
  - `real_path`: URL real encontrada en el HTML
  - `match_type`: Tipo de match (`exact`, `filename`, `path_segment`, `partial`, o `None`)

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
│         └─> Guarda raw_html y scraped_image_urls                    │
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
│   │                                                               │
│   └─> Para cada bundle:                                             │
│       ├─> Elimina ScrapedImageURL anteriores                        │
│       └─> Inserta nuevas ScrapedImageURL con metadatos             │
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
- `scraped_image_url.bundle_id` (INDEX)
- `scraped_image_url.scraped_date` (INDEX)
- `image_url.bundle_id` (INDEX)
- `image_url.image_type` (INDEX)
- `image_url.book_machine_name` (INDEX)

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

## Resumen de Características

### Ventajas del Sistema

1. **Arquitectura ETL Clara**: Separación bien definida entre extracción, transformación y carga
2. **Normalización Robusta**: Uso de pandas para limpieza y Pydantic para validación estricta
3. **Enriquecimiento de Datos**: Scraping detallado de cada bundle con resolución inteligente de URLs de imágenes
4. **Persistencia Eficiente**: UPSERT con ON CONFLICT para actualizar sin duplicados
5. **Trazabilidad**: Almacenamiento de HTML raw y metadatos de URLs scrapeadas para análisis posterior
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
