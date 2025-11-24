from functools import lru_cache
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuración de la aplicación para conexión a base de datos.
    
    Soporta tanto SQLite (desarrollo local) como PostgreSQL (producción).
    
    Atributos:
        db_type: Tipo de base de datos ('sqlite' o 'postgresql'). Por defecto 'sqlite'.
        db_path: Ruta al archivo de base de datos SQLite. Por defecto 'humble_bundle.db'.
        sql_echo: Si True, imprime las consultas SQL. Por defecto False.
        
        Para PostgreSQL:
        pguser: Usuario de PostgreSQL.
        pgpassword: Contraseña de PostgreSQL.
        pgdatabase: Nombre de la base de datos PostgreSQL.
        pghost: Host de PostgreSQL. Por defecto 'localhost'.
        pgport: Puerto de PostgreSQL. Por defecto 5432.
    
    Las variables de entorno deben tener el prefijo 'DB_' (ej: DB_DB_PATH, DB_PGUSER).
    """
    db_type: Literal['sqlite', 'postgresql'] = 'sqlite'
    db_path: str = 'humble_bundle.db'
    sql_echo: bool = False
    
    # PostgreSQL settings (opcionales, solo necesarios si db_type='postgresql')
    pguser: str | None = None
    pgpassword: str | None = None
    pgdatabase: str | None = None
    pghost: str = 'localhost'
    pgport: int = 5432

    model_config = SettingsConfigDict(
        env_prefix='DB_',
        env_file='.env',
        env_file_encoding='utf-8',
    )


@lru_cache
def get_settings() -> Settings:
    """
    Obtiene la configuración de la aplicación.
    
    La configuración se carga desde variables de entorno con prefijo 'DB_'
    o desde un archivo .env. El resultado se cachea para evitar múltiples
    lecturas de configuración.
    
    Returns:
        Instancia de Settings con la configuración cargada.
    """
    return Settings()

