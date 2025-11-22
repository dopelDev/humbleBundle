from datetime import datetime
from typing import Iterable

import logging
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, database_exists, drop_database
from sqlalchemy.dialects.postgresql import insert

from ..config.settings import Settings
from ..schemas.bundle import BundleRecord
from ..schemas.raw_data import LandingPageRawDataRecord
from .models import Base, Bundle, LandingPageRawData
from .session import build_database_uri

logger = logging.getLogger(__name__)


def ensure_landing_page_raw_data_table(engine) -> None:
    """
    Verifica y crea la tabla landing_page_raw_data si no existe.
    
    Args:
        engine: Motor de SQLAlchemy para ejecutar las consultas.
    """
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    
    if 'landing_page_raw_data' not in table_names:
        logger.info('Creando tabla landing_page_raw_data...')
        try:
            with engine.begin() as connection:
                connection.execute(text("""
                    CREATE TABLE landing_page_raw_data (
                        id UUID NOT NULL,
                        json_data JSONB NOT NULL,
                        scraped_date TIMESTAMP WITHOUT TIME ZONE NOT NULL,
                        source_url VARCHAR NOT NULL,
                        json_hash VARCHAR,
                        json_version VARCHAR,
                        PRIMARY KEY (id)
                    )
                """))
                connection.execute(text('CREATE INDEX ix_landing_page_raw_data_scraped_date ON landing_page_raw_data (scraped_date)'))
                connection.execute(text('CREATE INDEX ix_landing_page_raw_data_json_hash ON landing_page_raw_data (json_hash)'))
                logger.info('Tabla landing_page_raw_data creada exitosamente')
        except Exception as exc:
            logger.warning('Error creando tabla landing_page_raw_data (puede que ya exista): %s', exc)
    else:
        logger.debug('La tabla landing_page_raw_data ya existe')


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
    """
    Persiste los bundles en la base de datos.
    
    Inserta o actualiza los bundles usando machine_name como clave única.
    
    Args:
        records: Iterable de BundleRecord a persistir.
        session: Sesión de SQLAlchemy para la transacción.
        
    Raises:
        RuntimeError: Si ocurre un error al guardar los bundles en la BD.
    """
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


def persist_landing_page_raw_data(record: LandingPageRawDataRecord, session: Session) -> None:
    """
    Persiste el raw data de landingPage-json-data en la base de datos.
    
    Inserta un nuevo registro con el JSON raw obtenido del script
    landingPage-json-data junto con su metadata.
    
    Args:
        record: LandingPageRawDataRecord con el JSON y metadata a persistir.
        session: Sesión de SQLAlchemy para la transacción.
        
    Raises:
        RuntimeError: Si ocurre un error al guardar el raw data en la BD.
    """
    payload = record.to_orm_payload()
    try:
        landing_page_raw_data = LandingPageRawData(**payload)
        session.add(landing_page_raw_data)
        session.commit()
        logger.info('Raw data de landingPage guardado exitosamente')
    except SQLAlchemyError as exc:
        session.rollback()
        raise RuntimeError(f'Error guardando raw data de landingPage: {exc}') from exc


def remove_outdated_bundles(session: Session) -> None:
    """
    Elimina los bundles que han expirado de la base de datos.
    
    Un bundle se considera expirado si su fecha de fin (end_date_datetime)
    es anterior a la fecha/hora actual.
    
    Args:
        session: Sesión de SQLAlchemy para la transacción.
    """
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
    ensure_landing_page_raw_data_table(engine)
    logger.info('Base de datos recreada exitosamente')
