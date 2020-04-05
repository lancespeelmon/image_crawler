import abc
import logging
import multiprocessing
from logging import Logger
from typing import List

from .fbi_crawler import FbiCrawler
from .html_crawler import HtmlCrawler
from .interpol_crawler import InterpolCrawler

FBI_UNIT = {
    'crawler': FbiCrawler,
    'targets': [
        'https://www.fbi.gov/wanted/topten',
        # 'https://www.fbi.gov/wanted/terrorism',
        # 'https://www.fbi.gov/wanted/kidnap',
        # 'https://www.fbi.gov/wanted/seeking-information',
        # 'https://www.fbi.gov/wanted/parental-kidnappings',
        # 'https://www.fbi.gov/wanted/bank-robbers',
    ],
}

INTERPOL_UNIT = {
    'crawler': InterpolCrawler,
    'targets': [
        'https://www.interpol.int/en/How-we-work/Notices/View-Red-Notices',
    ],
}


class CrawlerConfig(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'logger')
                and callable(subclass.logger)
                and hasattr(subclass, 'workload')
                and callable(subclass.workload)
                and hasattr(subclass, 'concurrency')
                and callable(subclass.concurrency)
                and hasattr(subclass, 'crawler')
                and callable(subclass.crawler)
                or NotImplemented)

    _logger = None
    _crawlers = {}

    def __init__(self, logger: Logger):
        self._logger = logger
        self._crawlers[HtmlCrawler] = HtmlCrawler(logger)
        self._crawlers[FbiCrawler] = FbiCrawler(logger)
        self._crawlers[InterpolCrawler] = InterpolCrawler(logger)

    @classmethod
    def logger(self) -> logging.Logger:
        """Logger getter"""

        return self._logger

    @classmethod
    def workload(self) -> List[dict]:
        """Get configured workload"""

        return [FBI_UNIT, INTERPOL_UNIT]

    @classmethod
    def concurrency(self) -> int:
        """Get recommended concurrency for execution."""

        return min(len(self.workload()), multiprocessing.cpu_count())

    @classmethod
    def crawler(self, t: type) -> int:
        """Crawler factory for a given type."""

        return self._crawlers.get(t)
