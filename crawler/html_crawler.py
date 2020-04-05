import mimetypes
import re
import uuid
from typing import List

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

    def __init__(self):
        super().__init__()
        mimetypes.init()
        self._session = Session()

    def guess_file_extension(self, content_type: str):
        ''' Guess the file extension based on MIME content-type '''

        return mimetypes.guess_extension(content_type)

    def download_file(self, url: str) -> str:
        ''' Downloand a file from a URL '''

        regex = '''https://www.fbi.gov/wanted/topten/([0-9A-Za-z-]+)/@@images/image/preview'''
        filename: str = None
        destination: str = None
        match = re.search(regex, url)
        if match:
            filename = match.group(1)
        else:
            self._logger.warning("Could not determine filename for: %s", url)
            filename = str(uuid.uuid4())
        try:
            r = self._session.get(url, allow_redirects=True)
            ext = self.guess_file_extension(r.headers.get('content-type'))
            destination = f"output/{filename}{ext}"
            self._logger.info("write file: %s", destination)
            with open(destination, 'wb') as file:
                file.write(r.content)
        except Exception as e:
            raise e
        return destination

    def find_img_tags(self, soup: BeautifulSoup):
        """Find all img tags in HTML and return src attribute."""

        hits: List[str] = []
        for img in soup.find_all('img'):
            src: str = img.get('src')
            hits.append(src)
            self._logger.debug("add hit: %s", src)
        return hits

    def crawl(self, urls: List[str]) -> (int, List[Exception]):
        """Search the HTML for img tags."""

        files_downloaded = 0
        exceptions = []
        for url in urls:
            self._logger.debug("url = %s", url)
            page: Response = self._session.get(url)
            soup: BeautifulSoup = BeautifulSoup(page.content, 'html.parser')
            img_links: List[str] = self.find_img_tags(soup)
            for url in img_links:
                try:
                    self.download_file(url)
                    files_downloaded += 1
                except Exception as e:
                    exceptions.append(e)
        return(files_downloaded, exceptions)
