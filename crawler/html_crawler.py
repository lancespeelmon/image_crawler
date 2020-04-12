import hashlib
import mimetypes
from logging import Logger
from typing import List
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from requests import Session

from .crawler import Crawler


class HtmlCrawler(Crawler):
    """Inherits from Crawler."""

    _session: Session = None
    _ignore_file_types = [".svg"]

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

    def guess_file_extension(self, content_type: str):  # pylint: disable=R0201
        ''' Guess the file extension based on MIME content-type '''

        self._logger.debug("guess extension: %s", content_type)
        ext: str = mimetypes.guess_extension(content_type, strict=False)
        if not ext:
            self._logger.warning("Could not determine file extension for: %s", content_type)
        return ext

    def download_file(self, url: str) -> str:
        ''' Downloand a file from a URL '''

        filename: str = None
        destination: str = None
        # sha1 hash based on full img src url
        filename = hashlib.sha1(url.encode('utf-8')).hexdigest()
        destination = "output/" + filename
        try:
            res = self._session.get(url, allow_redirects=True)
            ext = self.guess_file_extension(res.headers.get('content-type'))
            if ext not in self._ignore_file_types:
                destination = (destination + ext) if ext else destination
                self._logger.info("write file: %s", destination)
                with open(destination, 'wb') as file:
                    file.write(res.content)
        except Exception as ex:
            raise ex
        return destination

    def find_img_tags(self, soup: BeautifulSoup, url):  # pylint: disable=R0201
        """Find all img tags in HTML and return src attribute."""

        if not url:
            raise ValueError("url is required!")

        hits: List[str] = []
        for img in soup.find_all('img'):
            src: str = urljoin(url, img.get('src'))
            if not (src.startswith("data:image/svg+xml;")  # ignore svg for now
                    or src.lower().endswith(".svg")
                    ):
                hits.append(src)
        return hits

    def get_content(self, url: str) -> bytes:
        """Download and return page content.
        """
        if not url:
            raise ValueError("url is required")
        self._logger.info("url: %s", url)
        return (self._session.get(url)).content

    def crawl(self, urls: List[str]) -> (int, List[Exception]):
        """Search the HTML for img tags."""

        files_downloaded = 0
        exceptions = []
        for url in urls:
            self._logger.info("url: %s", url)
            content = self.get_content(url)
            soup: BeautifulSoup = BeautifulSoup(content, 'html.parser')
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
