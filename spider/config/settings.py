from functools import lru_cache
from typing import Literal
from pydantic import Field
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

    jwt_secret_key: str = Field('change-me', description='Clave para firmar tokens JWT')
    jwt_algorithm: str = Field('HS256', description='Algoritmo de firma JWT')
    jwt_access_token_exp_minutes: int = Field(60, description='Minutos de expiración para el token de acceso')

    # Admin bootstrap (opcional)
    admin_username: str | None = Field(None, description='Usuario inicial para seed automático')
    admin_email: str | None = Field(None, description='Email del usuario inicial')
    admin_password_sha: str | None = Field(None, description='Hash SHA-256 generado en frontend')
    admin_password_plain: str | None = Field(None, description='Contraseña en texto plano (desarrollo)')

    model_config = SettingsConfigDict(
        env_prefix='DB_',
        env_file='.env',
        env_file_encoding='utf-8',
        extra='allow',
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

