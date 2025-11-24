"""
Módulo spider para scraping y procesamiento de bundles de Humble Bundle.
"""

# Exportaciones principales para mantener compatibilidad
from .core.spider import HumbleSpider
from .core.errors import HumbleSpiderError
from .database.models import Base, Bundle, LandingPageRawData
from .schemas.bundle import BundleRecord
from .schemas.raw_data import LandingPageRawDataRecord
from .database.persistence import (
    persist_bundles,
    remove_outdated_bundles,
    recreate_database,
    ensure_columns,
    persist_landing_page_raw_data,
    ensure_landing_page_raw_data_table,
)
from .database.session import get_session_factory, build_database_uri
from .config.settings import Settings, get_settings

__all__ = [
    # Core
    'HumbleSpider',
    'HumbleSpiderError',
    # Database
    'Base',
    'Bundle',
    'LandingPageRawData',
    'get_session_factory',
    'build_database_uri',
    'persist_bundles',
    'remove_outdated_bundles',
    'recreate_database',
    'ensure_columns',
    'persist_landing_page_raw_data',
    'ensure_landing_page_raw_data_table',
    # Schemas
    'BundleRecord',
    'LandingPageRawDataRecord',
    # Config
    'Settings',
    'get_settings',
]
