from hashlib import sha256


def sha256_hex(value: str) -> str:
    return sha256(value.encode("utf-8")).hexdigest()


__all__ = ["sha256_hex"]

