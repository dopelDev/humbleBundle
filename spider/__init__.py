"""
Módulo spider para scraping y procesamiento de bundles de Humble Bundle.
"""

# Exportaciones principales para mantener compatibilidad
from .core.spider import HumbleSpider
from .core.errors import HumbleSpiderError, ImageUrlScraperError
from .database.models import Base, Bundle, ScrapedImageURL, ImageURL
from .schemas.bundle import BundleRecord
from .database.persistence import (
    persist_bundles,
    remove_outdated_bundles,
    recreate_database,
    ensure_columns,
    ensure_image_url_table,
    ensure_scraped_image_url_table,
)
from .database.session import get_session_factory, build_database_uri
from .config.settings import Settings, get_settings

__all__ = [
    # Core
    'HumbleSpider',
    'HumbleSpiderError',
    'ImageUrlScraperError',
    # Database
    'Base',
    'Bundle',
    'ScrapedImageURL',
    'ImageURL',
    'get_session_factory',
    'build_database_uri',
    'persist_bundles',
    'remove_outdated_bundles',
    'recreate_database',
    'ensure_columns',
    'ensure_image_url_table',
    'ensure_scraped_image_url_table',
    # Schemas
    'BundleRecord',
    # Config
    'Settings',
    'get_settings',
]

