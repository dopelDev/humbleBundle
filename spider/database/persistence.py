from datetime import datetime
from typing import Iterable, List

import logging
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, database_exists, drop_database
from sqlalchemy.dialects.postgresql import insert

from ..config.settings import Settings
from ..schemas.bundle import BundleRecord
from .models import Base, Bundle
from .session import build_database_uri

logger = logging.getLogger(__name__)


def ensure_scraped_image_url_table(engine) -> None:
    """Verifica y crea la tabla scraped_image_url si no existe."""
    from sqlalchemy import inspect, text
    
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    
    if 'scraped_image_url' not in table_names:
        logger.info('Creando tabla scraped_image_url...')
        try:
            with engine.begin() as connection:
                connection.execute(text("""
                    CREATE TABLE scraped_image_url (
                        id UUID NOT NULL,
                        bundle_id UUID NOT NULL,
                        url VARCHAR NOT NULL,
                        source VARCHAR,
                        attribute VARCHAR,
                        scraped_date TIMESTAMP WITHOUT TIME ZONE NOT NULL,
                        PRIMARY KEY (id),
                        FOREIGN KEY (bundle_id) REFERENCES bundle (id) ON DELETE CASCADE
                    )
                """))
                connection.execute(text('CREATE INDEX ix_scraped_image_url_bundle_id ON scraped_image_url (bundle_id)'))
                connection.execute(text('CREATE INDEX ix_scraped_image_url_scraped_date ON scraped_image_url (scraped_date)'))
                logger.info('Tabla scraped_image_url creada exitosamente')
        except Exception as exc:
            logger.warning('Error creando tabla scraped_image_url (puede que ya exista): %s', exc)
    else:
        logger.debug('La tabla scraped_image_url ya existe')


def ensure_image_url_table(engine) -> None:
    """Verifica y crea la tabla image_url si no existe."""
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    
    if 'image_url' not in table_names:
        logger.info('Creando tabla image_url...')
        try:
            with engine.begin() as connection:
                connection.execute(text("""
                    CREATE TABLE image_url (
                        id UUID NOT NULL,
                        bundle_id UUID NOT NULL,
                        image_type VARCHAR NOT NULL,
                        book_machine_name VARCHAR,
                        original_url VARCHAR NOT NULL,
                        real_path VARCHAR,
                        match_type VARCHAR,
                        verification_date TIMESTAMP WITHOUT TIME ZONE NOT NULL,
                        PRIMARY KEY (id),
                        FOREIGN KEY (bundle_id) REFERENCES bundle (id) ON DELETE CASCADE
                    )
                """))
                connection.execute(text('CREATE INDEX ix_image_url_bundle_id ON image_url (bundle_id)'))
                connection.execute(text('CREATE INDEX ix_image_url_image_type ON image_url (image_type)'))
                connection.execute(text('CREATE INDEX ix_image_url_book_machine_name ON image_url (book_machine_name)'))
                logger.info('Tabla image_url creada exitosamente')
        except Exception as exc:
            logger.warning('Error creando tabla image_url (puede que ya exista): %s', exc)
    else:
        logger.debug('La tabla image_url ya existe')


def ensure_columns(engine) -> None:
    inspector = inspect(engine)
    
    # Verificar que la tabla bundle existe antes de intentar obtener columnas
    if 'bundle' not in inspector.get_table_names():
        logger.warning('La tabla bundle no existe, se creará automáticamente')
        return
    
    try:
        columns = {column['name'] for column in inspector.get_columns('bundle')}
    except Exception as exc:
        logger.warning('No se pudieron obtener columnas de la tabla bundle: %s', exc)
        return
    
    statements = []
    if 'duration_days' not in columns:
        statements.append('ALTER TABLE bundle ADD COLUMN duration_days DOUBLE PRECISION')
    if 'is_active' not in columns:
        statements.append('ALTER TABLE bundle ADD COLUMN is_active BOOLEAN DEFAULT FALSE')
    if 'price_tiers' not in columns:
        statements.append('ALTER TABLE bundle ADD COLUMN price_tiers JSONB')
    if 'book_list' not in columns:
        statements.append('ALTER TABLE bundle ADD COLUMN book_list JSONB')
    if 'featured_image' not in columns:
        statements.append('ALTER TABLE bundle ADD COLUMN featured_image VARCHAR')
    if 'msrp_total' not in columns:
        statements.append('ALTER TABLE bundle ADD COLUMN msrp_total DOUBLE PRECISION')
    if 'raw_html' not in columns:
        statements.append('ALTER TABLE bundle ADD COLUMN raw_html TEXT')
    
    for stmt in statements:
        try:
            with engine.begin() as connection:
                connection.execute(text(stmt))
                logger.info('Columna agregada: %s', stmt)
        except Exception as exc:
            logger.warning('Error agregando columna %s: %s', stmt, exc)


def persist_bundles(records: Iterable[BundleRecord], session: Session) -> None:
    from ..scrapers.image_scraper import ScrapedImageUrlInfo
    from .models import ScrapedImageURL
    
    payloads = [record.to_orm_payload() for record in records]
    if not payloads:
        return
    stmt = insert(Bundle).values(payloads)
    update_columns = {
        column.name: getattr(stmt.excluded, column.name)
        for column in Bundle.__table__.columns
        if column.name not in ('id',)
    }
    stmt = stmt.on_conflict_do_update(index_elements=['machine_name'], set_=update_columns)
    try:
        session.execute(stmt)
        session.commit()
    except SQLAlchemyError as exc:
        session.rollback()
        raise RuntimeError(f'Error guardando bundles: {exc}') from exc
    
    # Guardar las URLs scrapeadas después de persistir los bundles
    try:
        # Obtener los bundles actualizados/creados para tener sus IDs
        machine_names = [payload['machine_name'] for payload in payloads]
        bundles = session.query(Bundle).filter(Bundle.machine_name.in_(machine_names)).all()
        bundle_map = {bundle.machine_name: bundle.id for bundle in bundles}
        
        # Eliminar URLs scrapeadas anteriores de estos bundles
        for bundle_id in bundle_map.values():
            session.query(ScrapedImageURL).filter(ScrapedImageURL.bundle_id == bundle_id).delete()
        
        # Guardar las nuevas URLs scrapeadas
        for record in records:
            scraped_urls: List[ScrapedImageUrlInfo] = getattr(record, '_scraped_image_urls', None)
            if scraped_urls:
                bundle_id = bundle_map.get(record.machine_name)
                if bundle_id:
                    for url_info in scraped_urls:
                        scraped_url = ScrapedImageURL(
                            bundle_id=bundle_id,
                            url=url_info.url,
                            source=url_info.source,
                            attribute=url_info.attribute,
                        )
                        session.add(scraped_url)
        
        session.commit()
        logger.info(f'Guardadas URLs scrapeadas para {len([r for r in records if getattr(r, "_scraped_image_urls", None)])} bundles')
    except Exception as exc:
        session.rollback()
        logger.warning(f'Error guardando URLs scrapeadas: {exc}')


def remove_outdated_bundles(session: Session) -> None:
    current_time = datetime.utcnow()
    session.query(Bundle).filter(Bundle.end_date_datetime < current_time).delete(synchronize_session=False)
    session.commit()


def recreate_database(settings: Settings, drop_existing: bool = True) -> None:
    """
    Elimina y recrea la base de datos.
    
    Args:
        settings: Configuración de la base de datos
        drop_existing: Si True, elimina la base de datos existente antes de crearla
    """
    uri = build_database_uri(settings)
    engine = create_engine(uri, echo=settings.sql_echo, future=True)
    
    if drop_existing and database_exists(engine.url):
        logger.info('Eliminando base de datos existente: %s', settings.pgdatabase)
        drop_database(engine.url)
    
    if not database_exists(engine.url):
        logger.info('Creando base de datos: %s', settings.pgdatabase)
        create_database(engine.url)
    
    logger.info('Creando tablas...')
    # Usar checkfirst=True para evitar conflictos
    Base.metadata.create_all(engine, checkfirst=True)
    ensure_columns(engine)
    ensure_image_url_table(engine)
    ensure_scraped_image_url_table(engine)
    logger.info('Base de datos recreada exitosamente')

