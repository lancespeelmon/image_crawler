from logging import Logger
from typing import List

from bs4 import BeautifulSoup

from .html_crawler import HtmlCrawler


class InterpolCrawler(HtmlCrawler):
    """Inherits from HtmlCrawler.
    """

    _ignore_patterns: List[str] = [  # ignore images that match these patterns
        "/bundles/interpolfront/",
        "/1/1/1/6/76111-12-eng-GB/RedNoticeEnLR.jpg",
    ]

    def __init__(self, logger: Logger):
        super().__init__(logger)

    def find_img_tags(self, soup: BeautifulSoup, url):
        """Find images from interpol.int website.
        """
        hits: List[str] = []
        results: List[str] = super().find_img_tags(soup, url)
        for hit in results:
            ignore_match = False
            for ignore_pattern in self._ignore_patterns:
                if ignore_pattern in hit:
                    ignore_match = True
                    break  # short circuit for loop
            if ignore_match:
                self._logger.debug("ignore hit: %s", hit)
            else:
                hits.append(hit)
        return hits
