import hashlib
import mimetypes
from logging import Logger
from typing import List
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from requests import Session
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from .crawler import Crawler


class HtmlCrawler(Crawler):
    """ Inherits from Crawler.
    """
    _session: Session = None
    _driver = None  # selenium webdriver

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'guess_file_extension')
                and callable(subclass.guess_file_extension)
                and hasattr(subclass, 'download_file')
                and callable(subclass.download_file)
                and hasattr(subclass, 'find_img_tags')
                and callable(subclass.find_img_tags)
                )

    def __init__(self, logger: Logger):
        super().__init__(logger)
        mimetypes.init()
        self._session = Session()

    def init_selenium(self):
        """ Initialize selenium webdriver.
        """
        if not self._driver:
            driver_options = Options()
            driver_options.headless = True
            self._driver = webdriver.Chrome(options=driver_options)

    def guess_file_extension(self, content_type: str) -> str:  # pylint: disable=R0201
        """ Guess the file extension based on MIME content-type.
        """
        self._logger.debug("guess extension: %s", content_type)
        ext: str = mimetypes.guess_extension(content_type, strict=False)
        if not ext:
            self._logger.warning("Could not determine file extension for: %s", content_type)
        return ext

    def download_file(self, url: str) -> str:
        """ Downloand a file from a URL.
        """
        filename: str = None
        destination: str = None
        # sha1 hash based on full img src url
        filename = hashlib.sha1(url.encode('utf-8')).hexdigest()
        destination = "output/" + filename
        try:
            res = self._session.get(url, allow_redirects=True)
            ext = self.guess_file_extension(res.headers.get('content-type'))
            destination = (destination + ext) if ext else destination
            self._logger.info("write file: %s", destination)
            with open(destination, 'wb') as file:
                file.write(res.content)
        except Exception as ex:
            raise ex
        return destination

    def find_img_tags(self, soup: BeautifulSoup, url, ignore=None) -> List[str]:  # pylint: disable=R0201
        """ Find all img tags in HTML and return src attribute.
        """
        hits: List[str] = []
        for img in soup.find_all('img'):
            src: str = urljoin(url, img.get('src'))
            if ignore:
                ignore_match = False
                for ignore_pattern in ignore:
                    if ignore_pattern in src:
                        ignore_match = True
                        break  # short circuit for loop
                if ignore_match:
                    self._logger.debug("ignore src: %s", src)
                else:
                    hits.append(src)
            else:
                hits.append(src)
        return hits

    def get_content(self, url: str, render=False) -> bytes:
        """ Download and return page content.
        """
        self._logger.info("get_content(%s, render=%s)", url, render)
        content = None
        if render:
            self.init_selenium()
            self._driver.get(url)
            content = self._driver.page_source
        else:
            content = (self._session.get(url)).content
        return content

    def crawl(self, urls: List[str], render=False, ignore=None) -> (int, List[Exception]):
        """ Search the HTML for img tags.
        """
        files_downloaded = 0
        exceptions = []
        for url in urls:
            self._logger.info("url: %s", url)
            content = self.get_content(url, render)
            soup: BeautifulSoup = BeautifulSoup(content, 'html.parser')
            img_links: List[str] = self.find_img_tags(soup, url, ignore)
            for img_url in img_links:
                try:
                    dest = self.download_file(img_url)
                    if dest:
                        files_downloaded += 1
                except Exception as ex:
                    exceptions.append(ex)
                    raise ex
        return(files_downloaded, exceptions)
