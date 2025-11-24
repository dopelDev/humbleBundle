import sys
from ..core.spider import HumbleSpider
from ..core.errors import HumbleSpiderError
from ..config.settings import get_settings
from ..database.session import get_session_factory
from ..database.persistence import (
    persist_bundles,
    remove_outdated_bundles,
    persist_landing_page_raw_data,
)


def main() -> None:
    """
    Punto de entrada principal para ejecutar el spider de Humble Bundle.
    
    Obtiene los bundles desde Humble Bundle, limpia los bundles expirados
    de la base de datos y persiste los nuevos bundles obtenidos.
    
    Raises:
        SystemExit: Si ocurre un error al ejecutar el spider.
    """
    settings = get_settings()
    spider = HumbleSpider()
    
    try:
        print('Iniciando HumbleSpider...')
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
        
        # Guardar raw data de landingPage
        raw_data_record = spider.get_raw_data_record()
        if raw_data_record:
            print('Persistiendo raw data de landingPage...')
            persist_landing_page_raw_data(raw_data_record, session)
        
        print('¡Proceso completado exitosamente!')


if __name__ == '__main__':
    main()
