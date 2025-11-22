from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuración de la aplicación para conexión a base de datos.
    
    Atributos:
        pguser: Usuario de PostgreSQL. Por defecto 'postgres'.
        pgpassword: Contraseña de PostgreSQL. Por defecto 'postgres'.
        pgdatabase: Nombre de la base de datos. Por defecto 'test'.
        pghost: Host de PostgreSQL. Por defecto 'localhost'.
        pgport: Puerto de PostgreSQL. Por defecto 5432.
        sql_echo: Si True, imprime las consultas SQL. Por defecto False.
    
    Las variables de entorno deben tener el prefijo 'DB_' (ej: DB_PGUSER).
    """
    pguser: str = 'postgres'
    pgpassword: str = 'postgres'
    pgdatabase: str = 'test'
    pghost: str = 'localhost'
    pgport: int = 5432
    sql_echo: bool = False

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

