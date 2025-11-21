"""Modelos de base de datos y persistencia."""

from .models import Base, Bundle, ScrapedImageURL, ImageURL
from .session import get_session_factory, build_database_uri
from .persistence import (
    persist_bundles,
    remove_outdated_bundles,
    recreate_database,
    ensure_columns,
    ensure_image_url_table,
    ensure_scraped_image_url_table,
)

__all__ = [
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
]

