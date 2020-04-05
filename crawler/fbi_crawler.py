from logging import Logger
from typing import List

from bs4 import BeautifulSoup

from .html_crawler import HtmlCrawler


class FbiCrawler(HtmlCrawler):
    """Inherits from HtmlCrawler."""

    def __init__(self, logger: Logger):
        super().__init__(logger)

    def find_img_tags(self, soup: BeautifulSoup, url):
        ''' Find wanted images from fbi.gov website. '''

        hits: List[str] = []
        results: List[str] = super().find_img_tags(soup, url)
        for hit in results:
            if "/wanted/" in hit:  # filter only wanted images
                hits.append(hit)
            else:
                self._logger.debug("ignore hit: %s", hit)
        return hits
