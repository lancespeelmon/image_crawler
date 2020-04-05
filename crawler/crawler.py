import abc
from logging import Logger
from typing import List


class Crawler(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'crawl')
                and callable(subclass.crawl)
                or NotImplemented)

    _logger = None

    def __init__(self, logger: Logger):
        self._logger = logger

    @abc.abstractmethod
    def crawl(self, urls: List[str]) -> (int, List[Exception]):
        """Crawl the list of URLs"""
        raise NotImplementedError
