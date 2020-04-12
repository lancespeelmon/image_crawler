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

    def crawl(self, urls: List[str]) -> (int, List[Exception]):
        """Search the HTML for img tags."""

        files_downloaded = 0
        exceptions = []
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        for url in urls:
            self._logger.info("scrape: %s", url)
            driver.get(url)
            soup: BeautifulSoup = BeautifulSoup(driver.page_source, 'html.parser')
            img_links: List[str] = self.find_img_tags(soup, url)
            for img_url in img_links:
                try:
                    dest = self.download_file(img_url)
                    if dest:
                        files_downloaded += 1
                except Exception as ex:
                    exceptions.append(ex)
                    raise ex
        return(files_downloaded, exceptions)
