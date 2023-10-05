from humble_spider import HumbleSpider
from .settings import get_settings
from .dumpdata import get_session_factory, parse_sql

if __name__ == '__main__':
    spider = HumbleSpider()
    data  = spider.parser(spider.content)
    session = get_session_factory(get_settings())
    parse_sql(data, session)

