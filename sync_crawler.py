#!/usr/bin/env python3

import time

from crawler.config import CrawlerConfig
from crawler.crawler import Crawler
from logger.logger import get_logger

LOGGER = get_logger()
CONFIG = CrawlerConfig(LOGGER, max_depth=1)


def worker(unit: dict):
    crawler: Crawler = unit['crawler']
    try:
        (files_downloaded, exceptions) = crawler.crawl(unit['targets'])
        LOGGER.info("Downloaded %s files", files_downloaded)
        if exceptions:
            LOGGER.error("found %s errors!", len(exceptions))
            for ex in exceptions:
                LOGGER.error(ex)
    except Exception as ex:
        raise ex


def main():
    started_at = time.monotonic()
    for unit in CONFIG.workload:
        worker(unit)
    elasped_time = time.monotonic() - started_at

    LOGGER.info("Elapsed time: %.2f", elasped_time)


if __name__ == "__main__":
    main()
