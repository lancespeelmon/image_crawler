import multiprocessing
from typing import List

from crawler.config import CrawlerConfig
from crawler.crawler import Crawler
from logger.logger import get_logger

LOGGER = get_logger()
CC = CrawlerConfig(LOGGER)


def test_init():
    assert CC, "CrawlerConfig should not be None"
    assert CC.logger is LOGGER, "logger should be same as assigned"


def test_concurrency():
    concurrency = CC.concurrency
    assert concurrency > 0, "concurrency should be greater than 0"
    assert concurrency <= multiprocessing.cpu_count(), "concurrency should be less than or equal to number of CPUs"


def test_workload():
    workload: List[dict] = CC.workload
    assert workload, "workload should not be None"
    assert len(workload) > 0, "workload should have at least one item"
    crawler = workload[0]['crawler']
    assert crawler, "workload.crawler should not be None"
    assert isinstance(crawler, Crawler), "crawler should be a subclass of Crawler"
    targets = workload[0]['targets']
    assert targets, "workload.targets should not be None"
    assert isinstance(targets, List), "workload.targets should be a List"
    assert isinstance(targets[0], str), "workload.targets should have at least one String"
