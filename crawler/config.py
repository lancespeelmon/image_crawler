import abc
import logging
import multiprocessing
from logging import Logger
from typing import List

from .html_crawler import HtmlCrawler

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

    def __init__(self, logger: Logger, max_depth=3, think_time=5):
        self._logger = logger
        self.fbi_unit = {
            'targets': [
                'https://www.fbi.gov/wanted/topten',
            ],
            'crawler': HtmlCrawler(self._logger, render=False, follow_href_patterns=[
                'wanted/topten',
                'wanted/fugitives',
                'wanted/terrorism',
                'wanted/kidnap',
                'wanted/seeking-info',
                'wanted/parental-kidnappings',
                'wanted/bank-robbers',
                'wanted/ecap',
                'wanted/vicap',
            ], ignore=['theme/images/fbibannerseal.png'], max_depth=max_depth, think_time=think_time),
        }

    @property
    def logger(self) -> logging.Logger:
        """ logger getter
        """
        return self._logger

    @property
    def workload(self) -> List[dict]:  # pylint: disable=R0201
        """ Get configured workload.
        """
        return [self.fbi_unit]

    @property
    def concurrency(self) -> int:
        """ Get recommended concurrency for workload execution.
        """
        return min(len(self.workload), multiprocessing.cpu_count())
