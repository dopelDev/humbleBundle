from ..core.spider import HumbleSpider
from ..core.errors import HumbleSpiderError
from ..config.settings import get_settings
from ..database.session import get_session_factory
from ..database.persistence import persist_bundles, remove_outdated_bundles


def main() -> None:
    settings = get_settings()
    spider = HumbleSpider()
    
    try:
        print('Iniciando spider...')
        records = spider.fetch_bundles()
        print(f'Bundles obtenidos: {len(records)}')
    except HumbleSpiderError as exc:
        raise SystemExit(f'Error ejecutando el spider: {exc}') from exc

    SessionFactory = get_session_factory(settings)
    with SessionFactory() as session:
        print('Limpiando bundles expirados...')
        remove_outdated_bundles(session)
        print('Persistiendo bundles...')
        persist_bundles(records, session)
        print('¡Proceso completado exitosamente!')


if __name__ == '__main__':
    main()

