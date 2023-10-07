from humble_spider import HumbleSpider
from settings import get_settings
from dumpdata import get_session_factory, parse_sql, remove_outdated_bundles

if __name__ == '__main__':
    spider = HumbleSpider()
    data  = spider.parser(spider.content)
    session = get_session_factory(get_settings())
    with session:
        remove_outdated_bundles(session)
        parse_sql(data, session)

