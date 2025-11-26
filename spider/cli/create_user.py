import argparse
import sys

from spider.config.settings import get_settings
from spider.database.session import get_session_factory
from spider.database.seed import ensure_user


def parse_args():
    parser = argparse.ArgumentParser(
        description="Crea o actualiza un usuario en la base de datos. Puedes pasar contraseña en texto plano o SHA-256."
    )
    parser.add_argument("--username", required=True, help="Nombre de usuario (único)")
    parser.add_argument("--email", required=True, help="Email del usuario")
    parser.add_argument(
        "--password",
        required=True,
        help="Contraseña en texto plano o SHA-256 (64 chars). El backend la normaliza automáticamente.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    settings = get_settings()
    SessionFactory = get_session_factory(settings)
    with SessionFactory() as session:
        ensure_user(session, args.username.strip(), args.email.strip(), args.password.strip())


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Error creando usuario: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

