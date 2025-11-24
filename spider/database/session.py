import logging
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from ..config.settings import Settings
from .models import Base

logger = logging.getLogger(__name__)


def build_database_uri(settings: Settings) -> str:
    """
    Construye la URI de conexión a la base de datos SQLite.
    
    Args:
        settings: Configuración con la ruta al archivo SQLite.
        
    Returns:
        URI de conexión en formato sqlite:///
    """
    db_path = Path(settings.db_path)
    # Crear directorio si no existe
    db_path.parent.mkdir(parents=True, exist_ok=True)
    # Usar ruta absoluta para SQLite
    return f'sqlite:///{db_path.absolute()}'


def get_session_factory(settings: Settings):
    """
    Crea y configura una factory de sesiones de SQLAlchemy para SQLite.
    
    Crea las tablas necesarias si no existen y asegura que todas las columnas
    y tablas relacionadas estén presentes.
    
    Args:
        settings: Configuración con la ruta al archivo SQLite.
        
    Returns:
        sessionmaker configurado para crear sesiones de SQLAlchemy.
    """
    uri = build_database_uri(settings)
    engine = create_engine(uri, echo=settings.sql_echo, future=True, connect_args={'check_same_thread': False})
    
    # Crear todas las tablas si no existen
    logger.info('Creando tablas si no existen...')
    Base.metadata.create_all(engine, checkfirst=True)
    
    # Importar aquí para evitar importaciones circulares
    from .persistence import ensure_columns, ensure_landing_page_raw_data_table
    
    ensure_columns(engine)
    ensure_landing_page_raw_data_table(engine)
    return sessionmaker(bind=engine, expire_on_commit=False, class_=Session)
