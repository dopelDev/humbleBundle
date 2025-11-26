import re
from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from jose import JWTError, jwt
from passlib.context import CryptContext

from spider.config.settings import Settings
from spider.utils.crypto import sha256_hex

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
SHA256_REGEX = re.compile(r'^[a-fA-F0-9]{64}$')


def is_sha256_hash(value: str) -> bool:
    return bool(value) and bool(SHA256_REGEX.fullmatch(value))


def normalize_password_payload(password_input: str) -> str:
    """
    Normaliza la entrada de contraseña para garantizar bcrypt(SHA256(plain)).
    Si el valor ya es un hash SHA-256, lo devuelve tal cual; de lo contrario, lo hashea.
    """
    if is_sha256_hash(password_input):
        return password_input.lower()
    return sha256_hex(password_input)


def hash_password(password_input: str) -> str:
    normalized = normalize_password_payload(password_input)
    return pwd_context.hash(normalized)


def verify_password(password_input: str, stored_hash: str) -> bool:
    """
    Verifica la contraseña siempre como bcrypt(SHA256(plain)).
    """
    normalized = normalize_password_payload(password_input)
    return pwd_context.verify(normalized, stored_hash)


def create_access_token(
    data: Dict[str, Any],
    settings: Settings,
    expires_delta: timedelta | None = None,
) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.jwt_access_token_exp_minutes)
    )
    to_encode.update({'exp': expire})
    return jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(token: str, settings: Settings) -> Dict[str, Any]:
    return jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
    )


__all__ = [
    'is_sha256_hash',
    'sha256_hex',
    'hash_password',
    'verify_password',
    'create_access_token',
    'decode_access_token',
]

