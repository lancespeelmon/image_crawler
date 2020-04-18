import hashlib
import json
import mimetypes
import os
import random
import time
from functools import lru_cache
from logging import Logger
from typing import List
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from requests import Session
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

    def __init__(self, logger: Logger, max_depth=3, think_time=5):
        super().__init__(logger)
        mimetypes.init()
        self._session = Session()
        self.max_depth = max_depth  # max recursion depth
        self.headers = {'User-Agent': self.random_agent()}
        self.think_time = think_time

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
        """ Guess the file extension based on MIME content-type.
        """
        self._logger.debug("guess extension: %s", content_type)
        ext: str = mimetypes.guess_extension(content_type, strict=False)
        if not ext:
            self._logger.warning("Could not determine file extension for: %s", content_type)
        return ext

    def download_file(self, url: str, output='output') -> str:
        """ Download a file from a URL to the output directory.
        """
        destination: str = None
        # sha1 hash based on full img src url
        sha1_digest = hashlib.sha1(url.encode('utf-8')).hexdigest()
        destination = os.path.join(output, sha1_digest)
        try:
            time.sleep(random.randint(0, self.think_time))  # introduce some natural wait time
            res = self._session.get(url, headers=self.headers, allow_redirects=True)
            ext = self.guess_file_extension(res.headers.get('content-type'))
            metadata_file = destination + '-metadata.json'
            metadata = {
                'url': res.url,
                'headers': dict(res.headers),
                'status_code': res.status_code,
                'elasped_micros': str(res.elapsed.microseconds),
                'is_permanent_redirect': res.is_permanent_redirect,
                'is_redirect': res.is_redirect,
                'links': res.links,
                'reason': res.reason,
                'md5': hashlib.md5(url.encode('utf-8')).hexdigest(),
                'sha1': sha1_digest,
                'sha256': hashlib.sha256(url.encode('utf-8')).hexdigest(),
                'sha384': hashlib.sha384(url.encode('utf-8')).hexdigest(),
                'sha512': hashlib.sha512(url.encode('utf-8')).hexdigest(),
            }
            destination = (destination + ext) if ext else destination
            self._logger.info("write file: %s", destination)
            with open(destination, 'wb') as file:
                file.write(res.content)
            with open(metadata_file, 'w') as file:
                json.dump(metadata, file)
        except Exception as ex:
            raise ex
        return destination

    @lru_cache(maxsize=1000)
    def ignore_img(self, img_src: str, ignore: tuple) -> bool:
        """ Returns true if the image source should be ignored.
        """
        matched = False
        if ignore:
            for ignore_pattern in ignore:
                if ignore_pattern in img_src:
                    matched = True
                    break  # short circuit for loop
        return matched

    def find_img_tags(self, soup: BeautifulSoup, url, ignore=None) -> List[str]:  # pylint: disable=R0201
        """ Find all img tags in HTML and return src attribute.
        """
        for img in soup.find_all('img'):
            src: str = img.get('src')
            if not self.ignore_img(src, tuple(ignore)):
                yield urljoin(url, src)

    @lru_cache(maxsize=1000)
    def follow_href(self, href: str, follow: tuple) -> bool:
        """ Returns true if the href should be followed.
        """
        matched = False
        if follow:
            for follow_pattern in follow:
                if href.startswith('mailto:'):  # ignore mailto links
                    break
                if follow_pattern in href:
                    matched = True
                    break  # short circuit for loop
        else:  # Match on * if no patterns are passed
            matched = True
        return matched

    def find_a_tags(self, soup: BeautifulSoup, url, follow=None) -> List[str]:  # pylint: disable=R0201
        """ Find all anchor tags in HTML and return href attribute.
        """
        for a in soup.find_all('a'):
            href = a.get('href')
            if href and self.follow_href(href, follow):
                yield urljoin(url, href)

    @lru_cache(maxsize=100)
    def get_content(self, url: str, render=False) -> bytes:
        """ Download and return page content.
        """
        self._logger.info("url: %s", url)
        content = None
        if render:
            self.init_selenium()
            self._driver.get(url)
            content = self._driver.page_source
        else:
            head = self._session.head(url, headers=self.headers)
            if head.status_code == 200:
                content_type = head.headers['content-type']
                if 'text/html' in content_type.lower():
                    time.sleep(random.randint(0, self.think_time))  # introduce some natural wait time
                    content = (self._session.get(url, headers=self.headers)).content
            else:
                self._logger.info("ignored url: %s ; status_code=%s", url, head.status_code)
        return content

    def _crawl(self, url: str, render=False, ignore=None, follow_href=None,
               visited=[], img_links=set(), depth=0) -> List[str]:
        """ Recursive crawl web site for img tags.
        """
        if url in visited or depth > self.max_depth:  # base case
            return

        content = self.get_content(url, render)
        visited.append(url)
        if content:
            soup: BeautifulSoup = BeautifulSoup(content, 'html.parser')
            # add img links to results
            for link in self.find_img_tags(soup, url, ignore):
                img_links.add(link)
            # discover other links on page and recurse
            for link in self.find_a_tags(soup, url, follow_href):
                subj = link.lower()
                # TODO validate assumptions and make configurable
                if not (subj.endswith('.jpg') or subj.endswith('.pdf') or subj.endswith('.png')):
                    self._crawl(link, visited=visited, img_links=img_links, depth=depth + 1,
                                render=render, ignore=ignore, follow_href=follow_href)
        return img_links

    def crawl(self, urls: List[str], render=False, ignore=None, follow_href=None) -> (int, List[Exception]):
        """ Search the HTML for img tags.
        """
        files_downloaded = 0
        exceptions = []
        for url in urls:
            self._logger.info("url: %s", url)
            for img_url in self._crawl(url, render=render, ignore=ignore, follow_href=follow_href):
                try:
                    dest = self.download_file(img_url)
                    if dest:
                        files_downloaded += 1
                except Exception as ex:
                    exceptions.append(ex)
                    raise ex
        return(files_downloaded, exceptions)
