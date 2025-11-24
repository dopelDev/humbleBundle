from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuración de la aplicación para conexión a base de datos SQLite.
    
    Atributos:
        db_path: Ruta al archivo de base de datos SQLite. Por defecto 'humble_bundle.db'.
        sql_echo: Si True, imprime las consultas SQL. Por defecto False.
    
    Las variables de entorno deben tener el prefijo 'DB_' (ej: DB_DB_PATH).
    """
    db_path: str = 'humble_bundle.db'
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

