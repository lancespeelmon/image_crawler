from logging import Logger
from typing import List

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from .html_crawler import HtmlCrawler


class InterpolCrawler(HtmlCrawler):
    """Inherits from HtmlCrawler.
    """

    _ignore_patterns: List[str] = [  # ignore images that match these patterns
        "/bundles/interpolfront/",
        "/1/1/1/6/76111-12-eng-GB/RedNoticeEnLR.jpg",
    ]
    _options: Options = None
    _driver = None

    def __init__(self, logger: Logger):
        super().__init__(logger)
        self._options = Options()
        self._options.headless = True
        self._driver = webdriver.Chrome(options=self._options)

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

    def get_content(self, url: str) -> bytes:
        """Download and return page content.
        """
        if not url:
            raise ValueError("url is required")
        self._logger.info("url: %s", url)
        self._driver.get(url)
        return self._driver.page_source
