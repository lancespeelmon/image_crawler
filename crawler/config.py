import abc
import logging
import multiprocessing
from logging import Logger
from typing import List

from .html_crawler import HtmlCrawler

FBI_UNIT = {
    'crawler': HtmlCrawler,
    'render': False,
    'targets': [
        'https://www.fbi.gov/wanted/topten',
        # 'https://www.fbi.gov/wanted/terrorism',
        # 'https://www.fbi.gov/wanted/kidnap',
        # 'https://www.fbi.gov/wanted/seeking-information',
        # 'https://www.fbi.gov/wanted/parental-kidnappings',
        # 'https://www.fbi.gov/wanted/bank-robbers',
        # 'https://www.fbi.gov/wanted/ecap',
        # 'https://www.fbi.gov/wanted/vicap',
    ],
    'follow_href_patterns': [
        'wanted/topten',
        'wanted/fugitives',
        'wanted/terrorism',
        'wanted/kidnap',
        'wanted/seeking-info',
        'wanted/parental-kidnappings',
        'wanted/bank-robbers',
        'wanted/ecap',
        'wanted/vicap',
    ],
    'image_ignore_patterns': [
        'theme/images/fbibannerseal.png',
    ],
}

INTERPOL_UNIT = {
    'crawler': HtmlCrawler,
    'render': True,
    'targets': [
        'https://www.interpol.int/en/How-we-work/Notices/View-Red-Notices',
    ],
    'image_ignore_patterns': ['images/arrow-down.svg',
                              'images/arrow-up-stroke.svg',
                              'images/socials/Facebook.svg',
                              'images/socials/Twitter.svg',
                              'images/socials/Youtube.svg',
                              'images/socials/Instagram.svg',
                              'images/socials/LinkedIn.svg',
                              'images/socials/icon-Facebook.svg',
                              'images/socials/icon-Twitter.svg',
                              'interpolfront/images/rednotice',
                              'interpolfront/images/photo-not-available',
                              'interpolfront/images/logo-blanc',
                              'interpolfront/images/logo-text-only',
                              'images/1/1/1/6/76111-12-eng-GB/RedNoticeEnLR',
                              'interpolfront/images/logo.png',
                              'data:image/svg+xml',
                              ]
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
        # register _all_ available Crawlers
        self._crawlers[HtmlCrawler] = HtmlCrawler(logger)

    @property
    def logger(self) -> logging.Logger:
        """ logger getter
        """
        return self._logger

    @property
    def workload(self) -> List[dict]:  # pylint: disable=R0201
        """ Get configured workload.
        """
        return [FBI_UNIT]

    @property
    def concurrency(self) -> int:
        """ Get recommended concurrency for workload execution.
        """
        return min(len(self.workload), multiprocessing.cpu_count())

    def crawler(self, _type: type) -> int:
        """ Crawler factory for a given type.
        """
        return self._crawlers.get(_type)
