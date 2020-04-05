import hashlib
import mimetypes
from logging import Logger
from typing import List
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from requests import Response, Session

from .crawler import Crawler


class HtmlCrawler(Crawler):
    """Inherits from Crawler."""

    _session: Session = None

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

    def guess_file_extension(self, content_type: str):
        ''' Guess the file extension based on MIME content-type '''

        return mimetypes.guess_extension(content_type)

    def download_file(self, url: str) -> str:
        ''' Downloand a file from a URL '''

        filename: str = None
        destination: str = None
        # sha1 hash based on full img src url
        filename = hashlib.sha1(url.encode('utf-8')).hexdigest()
        try:
            r = self._session.get(url, allow_redirects=True)
            ext = self.guess_file_extension(r.headers.get('content-type'))
            if ext != ".svg":  # ignore svg files for now
                destination = f"output/{filename}{ext}"
                self._logger.info("write file: %s", destination)
                with open(destination, 'wb') as file:
                    file.write(r.content)
        except Exception as e:
            raise e
        return destination

    def find_img_tags(self, soup: BeautifulSoup, url):
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

    def crawl(self, urls: List[str]) -> (int, List[Exception]):
        """Search the HTML for img tags."""

        files_downloaded = 0
        exceptions = []
        for url in urls:
            self._logger.debug("url = %s", url)
            page: Response = self._session.get(url)
            soup: BeautifulSoup = BeautifulSoup(page.content, 'html.parser')
            img_links: List[str] = self.find_img_tags(soup, url)
            for url in img_links:
                try:
                    dest = self.download_file(url)
                    if dest:
                        files_downloaded += 1
                except Exception as e:
                    exceptions.append(e)
                    raise e
        return(files_downloaded, exceptions)
