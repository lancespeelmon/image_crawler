import abc
from logging import Logger
from typing import List


class Crawler(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return callable(subclass.crawl) if hasattr(subclass, 'crawl') else NotImplemented

    _logger = None

    def __init__(self, logger: Logger):
        self._logger = logger

    @property
    def logger(self) -> Logger:
        """ logger getter
        """
        return self._logger

    @abc.abstractmethod
    def crawl(self, urls: List[str], render=False, ignore=None, follow_href=None) -> (int, List[Exception]):
        """ Crawl the list of URLs.
        """
        raise NotImplementedError
