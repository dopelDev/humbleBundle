import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_utils import create_database, database_exists

from ..config.settings import Settings
from .models import Base

logger = logging.getLogger(__name__)


def build_database_uri(settings: Settings) -> str:
    return (
        f'postgresql+psycopg://{settings.pguser}:{settings.pgpassword}'
        f'@{settings.pghost}:{settings.pgport}/{settings.pgdatabase}'
    )


def get_session_factory(settings: Settings):
    uri = build_database_uri(settings)
    engine = create_engine(uri, echo=settings.sql_echo, future=True)
    if not database_exists(engine.url):
        create_database(engine.url)
    
    # Verificar si la tabla ya existe usando una consulta SQL directa
    # para evitar conflictos con tipos personalizados en PostgreSQL
    with engine.connect() as conn:
        try:
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'bundle'
                )
            """))
            table_exists = result.scalar()
            
            if not table_exists:
                logger.info('Creando tabla bundle...')
                Base.metadata.create_all(engine, checkfirst=True)
            else:
                logger.debug('La tabla bundle ya existe, omitiendo creación')
        except Exception as exc:
            logger.warning('Error verificando existencia de tabla: %s', exc)
            # Si hay error verificando, intentar crear con checkfirst como fallback
            try:
                Base.metadata.create_all(engine, checkfirst=True)
            except Exception as create_exc:
                logger.error('Error al crear tablas: %s', create_exc)
                # Si sigue fallando, asumir que la tabla existe y continuar
                logger.warning('Asumiendo que las tablas ya existen y continuando...')
    
    # Importar aquí para evitar importaciones circulares
    from .persistence import ensure_columns, ensure_image_url_table, ensure_scraped_image_url_table
    
    ensure_columns(engine)
    ensure_image_url_table(engine)
    ensure_scraped_image_url_table(engine)
    return sessionmaker(bind=engine, expire_on_commit=False, class_=Session)

