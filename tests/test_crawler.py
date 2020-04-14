from crawler.crawler import Crawler
from logger.logger import get_logger


def test_init():
    logger = get_logger()
    try:
        crawler = Crawler(logger)
        assert not crawler, "crawler is abstract and should be allowed to be instantiated"
    except TypeError as type_err:
        assert type_err, "TypeError is expected; crawler is abstract"
    except Exception as err:
        assert not err, "Exception should be of type TypeError"
