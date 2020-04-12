import multiprocessing
from typing import List

from crawler.config import CrawlerConfig
from logger.logger import get_logger
from crawler.crawler import Crawler
from crawler.html_crawler import HtmlCrawler

LOGGER = get_logger()
CC = CrawlerConfig(LOGGER)


def test_init():
    assert CC
    assert CC.logger() is LOGGER


def test_concurrency():
    concurrency = CC.concurrency()
    assert concurrency > 0
    assert concurrency <= multiprocessing.cpu_count()


def test_workload():
    workload: List[dict] = CC.workload()
    assert workload
    assert len(workload) > 0
    crawler = workload[0]['crawler']
    assert crawler
    assert issubclass(crawler, Crawler)
    targets = workload[0]['targets']
    assert targets
    assert isinstance(targets, List)
    assert isinstance(targets[0], str)


def test_crawler():
    crawler = CC.crawler(HtmlCrawler)
    assert crawler
    assert isinstance(crawler, Crawler)
