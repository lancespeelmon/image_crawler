from typing import List
from bs4 import BeautifulSoup
from .html_crawler import HtmlCrawler


@HtmlCrawler.register
class FbiCrawler(HtmlCrawler):
    """Inherits from HtmlCrawler."""

    def find_img_tags(self, soup: BeautifulSoup):
        ''' Find wanted images from fbi.gov website. '''

        hits: List[str] = []
        for img in soup.find_all('img'):
            src: str = img.get('src')
            if "/wanted/" in src:
                hits.append(src)
                self._logger.debug("add hit: %s", src)
        return hits
