import logging
from typing import Optional

from sqlalchemy.orm import Session

from spider.config.settings import Settings
from spider.database.models import User
from api.security import hash_password, verify_password

logger = logging.getLogger(__name__)


def ensure_user(session: Session, username: str, email: str, password_input: str) -> str:
    """
    Crea o actualiza un usuario con los datos proporcionados.
    """
    if not username or not email or not password_input:
        raise ValueError('username, email y password_input son obligatorios')

    hashed_password = hash_password(password_input)
    existing = session.query(User).filter(User.username == username).first()
    if existing:
        status = 'unchanged'
        if existing.email != email:
            existing.email = email
            status = 'updated'
        if not verify_password(password_input, existing.password_hash):
            existing.password_hash = hashed_password
            status = 'updated'
        if status == 'updated':
            session.commit()
            logger.info("Usuario '%s' actualizado.", username)
        else:
            logger.info("Usuario '%s' ya estaba al día.", username)
        return status

    user = User(
        username=username,
        email=email,
        password_hash=hashed_password,
    )
    session.add(user)
    session.commit()
    logger.info("Usuario '%s' creado.", username)
    return 'created'


def ensure_admin_user(session: Session, settings: Settings) -> None:
    """
    Crea o actualiza el usuario admin usando las variables de entorno configuradas.
    """
    username = (settings.admin_username or "").strip()
    email = (settings.admin_email or "").strip()
    password_plain = (settings.admin_password_plain or "").strip()
    password_sha = (settings.admin_password_sha or "").strip()

    if not username or not email:
        logger.debug("Seed admin: username/email no configurados, se omite.")
        return

    password_input = password_plain or password_sha
    if not password_input:
        logger.warning("Seed admin: define DB_ADMIN_PASSWORD_PLAIN o DB_ADMIN_PASSWORD_SHA para crear el usuario inicial.")
        return

    try:
        return ensure_user(session, username, email, password_input)
    except Exception as exc:
        logger.error("Seed admin: error creando/actualizando usuario (%s)", exc)
        return None

