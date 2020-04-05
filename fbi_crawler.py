#!/usr/bin/env python3

from logger.logger import get_logger
from crawler.crawler import Crawler
from crawler.fbi_crawler import FbiCrawler

LOGGER = get_logger()
URLS = [
    'https://www.fbi.gov/wanted/topten',
    # 'https://www.fbi.gov/wanted/terrorism',
    # 'https://www.fbi.gov/wanted/kidnap',
    # 'https://www.fbi.gov/wanted/seeking-information',
    # 'https://www.fbi.gov/wanted/parental-kidnappings',
    # 'https://www.fbi.gov/wanted/bank-robbers',
]


def main():
    crawler: Crawler = FbiCrawler()
    (files_downloaded, exceptions) = crawler.crawl(URLS)
    LOGGER.info("Downloaded %s files", files_downloaded)
    if exceptions:
        LOGGER.error("found %s errors!", len(exceptions))
        for e in exceptions:
            LOGGER.error(e.message, e)


if __name__ == "__main__":
    main()
