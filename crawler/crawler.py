import abc
from typing import List
from logger.logger import get_logger


class Crawler(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'crawl')
                and callable(subclass.crawl)
                or NotImplemented)

    _logger = None

    def __init__(self):
        self._logger = get_logger()

    @abc.abstractmethod
    def crawl(self, urls: List[str]) -> (int, List[Exception]):
        """Crawl the list of URLs"""
        raise NotImplementedError
