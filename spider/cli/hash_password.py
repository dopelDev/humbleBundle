import argparse

from spider.utils.crypto import sha256_hex


def parse_args():
    parser = argparse.ArgumentParser(
        description="Convierte una contraseña en su hash SHA-256 (hex)."
    )
    parser.add_argument("--password", required=True, help="Contraseña en texto plano")
    return parser.parse_args()


def main():
    args = parse_args()
    print(sha256_hex(args.password))


if __name__ == "__main__":
    main()

