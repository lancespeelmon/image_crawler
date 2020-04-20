import hashlib
import json
import mimetypes
import os
import random
import time
from functools import lru_cache
from logging import Logger
from os import path
from typing import List
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from requests import Response, Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from .crawler import Crawler

USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
]


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

    def __init__(self, logger: Logger, render=False, ignore=[], follow_href_patterns=[], max_depth=1, think_time=10,
                 http_retries=5, retry_backoff=5):
        super().__init__(logger)
        self.render = render
        self.ignore = ignore
        self.follow_href_patterns = follow_href_patterns
        self.max_depth = max_depth  # max recursion depth
        self.think_time = think_time

        self._session = Session()
        self.headers = {'User-Agent': self.random_agent()}
        retry_strategy = Retry(
            total=http_retries,
            backoff_factor=retry_backoff,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self._session.mount("https://", adapter)
        self._session.mount("http://", adapter)
        mimetypes.init()

    def init_selenium(self):
        """ Initialize selenium webdriver.
        """
        if not self._driver:
            driver_options = Options()
            driver_options.headless = True
            self._driver = webdriver.Chrome(options=driver_options)

    def random_agent(self) -> str:
        """ Returns a random browser agent string
        """
        idx = random.randint(0, len(USER_AGENTS) - 1)
        return USER_AGENTS[idx]

    def guess_file_extension(self, content_type: str) -> str:  # pylint: disable=R0201
        """ Guess the file extension based on MIME Content-Type.
        """
        ext: str = mimetypes.guess_extension(content_type, strict=False)
        if not ext:
            self._logger.warning("Could not determine file extension for: %s", content_type)
        return ext

    def cached(self, headers: dict, metadata_file: str, destination: str) -> bool:
        """ Do we already have asset in local cache?
        """
        asset_cached = False
        try:
            if path.exists(metadata_file):
                with open(metadata_file) as file:
                    metadata = json.load(file)
                    if (headers['Content-Type'] == metadata['headers']['Content-Type']
                            and headers['Content-Length'] == metadata['headers']['Content-Length']
                            and path.exists(destination)
                            and (os.stat(destination)).st_size == int(headers['Content-Length'])):
                        self._logger.info("Asset already cached locally: %s", destination)
                        asset_cached = True
                    else:
                        self._logger.debug("metadata did not match!: %s\n %s", headers, metadata)
            else:
                self._logger.debug("metadata_file not found: %s", metadata_file)
        except Exception as ex:
            self._logger.error(ex)
        return asset_cached

    def download_file(self, url: str, output='output') -> str:
        """ Download a file from a URL to the output directory.
        """
        destination: str = None
        # sha1 hash based on full img src url
        url_encoded = url.encode('utf-8')
        sha1_digest = hashlib.sha1(url_encoded).hexdigest()
        destination = os.path.join(output, sha1_digest)
        try:
            time.sleep(random.randint(0, self.think_time))  # introduce some natural wait time
            head: Response = self._session.head(url, headers=self.headers, allow_redirects=True)
            ext = self.guess_file_extension(head.headers.get('Content-Type'))
            metadata_file = destination + '-metadata.json'
            destination = (destination + ext) if ext else destination
            if not self.cached(dict(head.headers), metadata_file, destination):
                res: Response = self._session.get(url, headers=self.headers, allow_redirects=True)
                metadata = {
                    'url': res.url,
                    'headers': dict(res.headers),
                    'status_code': res.status_code,
                    'elapsed_microseconds': str(res.elapsed.microseconds),
                    'is_permanent_redirect': res.is_permanent_redirect,
                    'is_redirect': res.is_redirect,
                    'links': res.links,
                    'reason': res.reason,
                    'md5': hashlib.md5(url_encoded).hexdigest(),
                    'sha1': sha1_digest,
                    'sha256': hashlib.sha256(url_encoded).hexdigest(),
                    'sha384': hashlib.sha384(url_encoded).hexdigest(),
                    'sha512': hashlib.sha512(url_encoded).hexdigest(),
                }
                self._logger.info("write file: %s", destination)
                with open(destination, 'wb') as file:
                    file.write(res.content)
                with open(metadata_file, 'w') as file:
                    json.dump(metadata, file)
        except Exception as ex:
            raise ex
        return destination

    @lru_cache(maxsize=1000)
    def ignore_img(self, img_src: str) -> bool:
        """ Returns true if the image source should be ignored.
        """
        matched = False
        if self.ignore:
            for ignore_pattern in self.ignore:
                if ignore_pattern in img_src:
                    matched = True
                    break  # short circuit for loop
        return matched

    def find_img_tags(self, soup: BeautifulSoup, url: str) -> List[str]:  # pylint: disable=R0201
        """ Find all img tags in HTML and return src attribute.
        """
        for img in soup.find_all('img'):
            src: str = img.get('src')
            if not self.ignore_img(src):
                yield urljoin(url, src)

    @lru_cache(maxsize=1000)
    def follow_href(self, href: str) -> bool:
        """ Returns true if the href should be followed.
        """
        matched = False
        if self.follow_href_patterns:
            for follow_pattern in self.follow_href_patterns:
                if href.startswith('mailto:'):  # ignore mailto links
                    break
                if follow_pattern in href:
                    matched = True
                    break  # short circuit for loop
        else:  # Match on * if no patterns are passed
            matched = True
        return matched

    def find_a_tags(self, soup: BeautifulSoup, url: str) -> List[str]:  # pylint: disable=R0201
        """ Find all anchor tags in HTML and return href attribute.
        """
        for a in soup.find_all('a'):
            href = a.get('href')
            if href and self.follow_href(href):
                yield urljoin(url, href)

    @lru_cache(maxsize=100)
    def get_content(self, url: str) -> bytes:
        """ Download and return page content.
        """
        self._logger.info("url: %s", url)
        content = None
        if self.render:
            self.init_selenium()
            self._driver.get(url)
            content = self._driver.page_source
        else:
            head: Response = self._session.head(url, headers=self.headers)
            if head.status_code == 200:
                content_type = head.headers['Content-Type']
                if 'text/html' in content_type.lower():
                    time.sleep(random.randint(0, self.think_time))  # introduce some natural wait time
                    content = (self._session.get(url, headers=self.headers)).content
            else:
                self._logger.info("ignored url: %s ; status_code=%s", url, head.status_code)
        return content

    @lru_cache(maxsize=1000)
    def ignore_href(self, href: str):
        """ Should the href be ignored?
        """
        return href.lower().startswith('javascript:') or href.endswith('.jpg') or href.endswith('.pdf') or href.endswith('.png')

    def _crawl(self, url: str, visited=[], img_links=set(), depth=0) -> List[str]:
        """ Recursive crawl web site for img tags.
        """
        if url in visited or depth > self.max_depth:  # base case
            return

        content = self.get_content(url)
        visited.append(url)
        if content:
            soup: BeautifulSoup = BeautifulSoup(content, 'html.parser')
            # add img links to results
            for link in self.find_img_tags(soup, url):
                img_links.add(link)
            # discover other links on page and recurse
            for link in self.find_a_tags(soup, url):
                if not self.ignore_href(link):
                    self._crawl(link, visited=visited, img_links=img_links, depth=depth + 1)
        return img_links

    def crawl(self, urls: List[str]) -> (int, List[Exception]):
        """ Search the HTML for img tags.
        """
        files_downloaded = 0
        exceptions = []
        for url in urls:
            self._logger.info("url: %s", url)
            for img_url in self._crawl(url):
                try:
                    dest = self.download_file(img_url)
                    if dest:
                        files_downloaded += 1
                except Exception as ex:
                    exceptions.append(ex)
                    raise ex
        return(files_downloaded, exceptions)
