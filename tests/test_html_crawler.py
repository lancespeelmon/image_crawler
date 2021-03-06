import os
import re
from typing import List
from urllib.parse import quote

import pytest
from bs4 import BeautifulSoup
from requests_mock.mocker import Mocker

from crawler.config import CrawlerConfig
from crawler.html_crawler import HtmlCrawler
from logger.logger import get_logger


@pytest.fixture
def logger():
    return get_logger()


@pytest.fixture
def configuration(logger):
    return CrawlerConfig(logger)


@pytest.fixture
def crawler(logger):
    image_ignore_patterns = ['theme/images/fbibannerseal.png',
                             'images/arrow-down.svg',
                             'images/arrow-up-stroke.svg',
                             'images/socials/Facebook.svg',
                             'images/socials/Twitter.svg',
                             'images/socials/Youtube.svg',
                             'images/socials/Instagram.svg',
                             'images/socials/LinkedIn.svg',
                             'images/socials/icon-Facebook.svg',
                             'images/socials/icon-Twitter.svg',
                             'data:image/svg+xml',
                             ]
    follow_patterns = ('wanted/ecap', 'wanted/vicap', '/en/Crimes/Cybercrime')
    return HtmlCrawler(logger, think_time=0, follow_href_patterns=follow_patterns, ignore=image_ignore_patterns)


@pytest.fixture
def empty_ignore_crawler(logger):
    follow_patterns = ('wanted/ecap', 'wanted/vicap', '/en/Crimes/Cybercrime')
    return HtmlCrawler(logger, think_time=0, follow_href_patterns=follow_patterns)


@pytest.fixture
def empty_follow_crawler(logger):
    return HtmlCrawler(logger, think_time=0, follow_href_patterns=[])


def match_request_url(request) -> bool:
    ignored = ['https://www.fbi.gov/wanted/topten', 'https://www.interpol.int/en/How-we-work/Notices/View-Red-Notices']
    return request.url not in ignored


@pytest.fixture
def expectations(requests_mock: Mocker):
    """ Loads the mock data from tests/fixtures/<url>
    """
    expectations = {
        'https://www.fbi.gov/wanted/topten': {
            'content': None,  # lazy loaded below
            'img_links': ['https://www.fbi.gov/wanted/topten/yaser-abdel-said/@@images/image/preview',
                          'https://www.fbi.gov/wanted/topten/alexis-flores/@@images/image/preview',
                          'https://www.fbi.gov/wanted/topten/eugene-palmer/@@images/image/preview',
                          'https://www.fbi.gov/wanted/topten/santiago-mederos/@@images/image/preview',
                          'https://www.fbi.gov/wanted/topten/rafael-caro-quintero/@@images/image/preview',
                          'https://www.fbi.gov/wanted/topten/robert-william-fisher/@@images/image/preview',
                          'https://www.fbi.gov/wanted/topten/bhadreshkumar-chetanbhai-patel/@@images/image/preview',
                          'https://www.fbi.gov/wanted/topten/alejandro-castillo/@@images/image/preview',
                          'https://www.fbi.gov/wanted/topten/arnoldo-jimenez/@@images/image/preview',
                          'https://www.fbi.gov/wanted/topten/jason-derek-brown/@@images/image/preview'],
            'a_tags': ['https://www.fbi.gov/wanted/ecap',
                       'https://www.fbi.gov/wanted/vicap',
                       'https://www.fbi.gov/wanted/ecap',
                       'https://www.fbi.gov/wanted/vicap'],
        },
        'https://www.interpol.int/en/How-we-work/Notices/View-Red-Notices': {
            'content': None,  # lazy loaded below
            'img_links': ['https://www.interpol.int/bundles/interpolfront/images/logo.png',
                          'https://www.interpol.int/bundles/interpolfront/images/logo-text-only.png',
                          'https://www.interpol.int/var/interpol/storage/images/1/1/1/6/76111-12-eng-GB/RedNoticeEnLR.jpg',
                          'https://ws-public.interpol.int/notices/v1/red/2020-26948/images/61775574',
                          'https://www.interpol.int/bundles/interpolfront/images/rednotice.png',
                          'https://ws-public.interpol.int/notices/v1/red/2020-26190/images/61772589',
                          'https://www.interpol.int/bundles/interpolfront/images/rednotice.png',
                          'https://ws-public.interpol.int/notices/v1/red/2020-26878/images/61775241',
                          'https://www.interpol.int/bundles/interpolfront/images/rednotice.png',
                          'https://ws-public.interpol.int/notices/v1/red/2020-26860/images/61775167',
                          'https://www.interpol.int/bundles/interpolfront/images/rednotice.png',
                          'https://ws-public.interpol.int/notices/v1/red/2020-26825/images/61775048',
                          'https://www.interpol.int/bundles/interpolfront/images/rednotice.png',
                          'https://ws-public.interpol.int/notices/v1/red/2020-26239/images/61772781',
                          'https://www.interpol.int/bundles/interpolfront/images/rednotice.png',
                          'https://ws-public.interpol.int/notices/v1/red/2015-42824/images/59832553',
                          'https://www.interpol.int/bundles/interpolfront/images/rednotice.png',
                          'https://ws-public.interpol.int/notices/v1/red/2020-26247/images/61772803',
                          'https://www.interpol.int/bundles/interpolfront/images/rednotice.png',
                          'https://ws-public.interpol.int/notices/v1/red/2020-26214/images/61772666',
                          'https://www.interpol.int/bundles/interpolfront/images/rednotice.png',
                          'https://ws-public.interpol.int/notices/v1/red/2017-130054/images/61493233',
                          'https://www.interpol.int/bundles/interpolfront/images/rednotice.png',
                          'https://ws-public.interpol.int/notices/v1/red/2020-25875/images/61771543',
                          'https://www.interpol.int/bundles/interpolfront/images/rednotice.png',
                          'https://ws-public.interpol.int/notices/v1/red/2020-25867/images/61771519',
                          'https://www.interpol.int/bundles/interpolfront/images/rednotice.png',
                          'https://ws-public.interpol.int/notices/v1/red/2020-25861/images/61771500',
                          'https://www.interpol.int/bundles/interpolfront/images/rednotice.png',
                          'https://ws-public.interpol.int/notices/v1/red/2020-25587/images/61770497',
                          'https://www.interpol.int/bundles/interpolfront/images/rednotice.png',
                          'https://ws-public.interpol.int/notices/v1/red/2020-24211/images/61765539',
                          'https://www.interpol.int/bundles/interpolfront/images/rednotice.png',
                          'https://ws-public.interpol.int/notices/v1/red/2020-24051/images/61765027',
                          'https://www.interpol.int/bundles/interpolfront/images/rednotice.png',
                          'https://ws-public.interpol.int/notices/v1/red/2020-24000/images/61764808',
                          'https://www.interpol.int/bundles/interpolfront/images/rednotice.png',
                          'https://ws-public.interpol.int/notices/v1/red/2020-24062/images/61765096',
                          'https://www.interpol.int/bundles/interpolfront/images/rednotice.png',
                          'https://ws-public.interpol.int/notices/v1/red/2020-23879/images/61764455',
                          'https://www.interpol.int/bundles/interpolfront/images/rednotice.png',
                          'https://ws-public.interpol.int/notices/v1/red/2020-23364/images/61763068',
                          'https://www.interpol.int/bundles/interpolfront/images/rednotice.png',
                          'https://www.interpol.int/bundles/interpolfront/images/photo-not-available.png',
                          'https://www.interpol.int/bundles/interpolfront/images/rednotice.png',
                          'https://www.interpol.int/bundles/interpolfront/images/rednotice_big.png',
                          'https://www.interpol.int/bundles/interpolfront/images/photo-not-available.png',
                          'https://www.interpol.int/bundles/interpolfront/images/rednotice.png',
                          'https://www.interpol.int/bundles/interpolfront/images/logo-blanc.png'],
            'a_tags': ['https://www.interpol.int/en/Crimes/Cybercrime'],
        },
    }
    # mock page content
    headers = {'Content-Type': 'text/html; charset=utf-8'}
    matcher = re.compile('.gov/|interpol.int/|.com/')
    for url in expectations.keys():
        requests_mock.head(url, headers=headers)
        filename = (os.path.join(os.path.dirname(__file__), 'fixtures', quote(url, '')))
        with open(filename, 'r') as file:
            content = file.read()
            assert len(content) > 0, "content mock must have data"
            expectations[url]['content'] = content.encode('utf-8')
        requests_mock.get(url, text=content, headers=headers)
        requests_mock.register_uri('HEAD', matcher, additional_matcher=match_request_url, headers=headers)
        requests_mock.register_uri('GET', matcher, text=content, additional_matcher=match_request_url, headers=headers)
    # TODO add test coverage for 429 rate limit status_code with custom matcher
    return expectations


@pytest.fixture
def mock_images(requests_mock: Mocker):
    """ Loads the mock images from tests/fixtures/<image>
    """
    expectations = {}
    url = 'https://www.fbi.gov/wanted/topten/yaser-abdel-said/@@images/image/preview'
    filename = (os.path.join(os.path.dirname(__file__), 'fixtures', '1ce559cc3fa5dfd70d914a3f083b357c474fdf63.jpg'))
    with open(filename, 'rb') as file:
        jpeg = file.read()
        requests_mock.head(url, headers={'Content-Type': 'image/jpeg', 'Content-Length': '23930'})
        requests_mock.get(url, content=jpeg, headers={'Content-Type': 'image/jpeg', 'Content-Length': '23930'})
        expectations[url] = {}
        expectations[url]['content'] = jpeg
    return expectations


def test_init(logger, crawler):
    # happy path
    assert crawler, "crawler should not be None"
    assert crawler.logger is logger, "logger should be same as assigned"

    # illegal logger passed
    try:
        crawler = HtmlCrawler()
        assert not crawler, "TypeError should be raised if logger is None"
    except TypeError as type_err:
        assert type_err, "TypeError should be raised if logger is None"
    except Exception as err:
        assert not err, "Exception should be of type TypeError"


def test_guess_file_extension(crawler):
    # happy path
    assert crawler.guess_file_extension("image/jpeg") == ".jpg", "image/jpeg should return .jpg"
    assert crawler.guess_file_extension("image/png") == ".png", "image/png should return .png"
    # non-standard mime type
    assert crawler.guess_file_extension("image/jpg") == ".jpg", "image/jpg is not standard but should also return .jpg"
    # edge cases
    assert crawler.guess_file_extension("image/foober") is None, "unknown mime types should return None"
    try:
        ret_val = crawler.guess_file_extension()
        assert not ret_val, "TypeError should be raised if content_type is None"
    except TypeError as type_err:
        assert type_err, "TypeError should be raised if content_type is None"
    except Exception as err:
        assert not err, "Exception should be of type TypeError"


def test_get_content(crawler, expectations):
    for url in expectations.keys():
        content = crawler.get_content(url)
        assert len(content) > 0, "content must have data"
        assert content == expectations[url]['content'], "returned content must match source"

    try:
        content = crawler.get_content()
        assert not content, "TypeError should be raised if content_type is None"
    except TypeError as type_err:
        assert type_err, "TypeError should be raised if content_type is None"
    except Exception as err:
        assert not err, "Exception should be of type TypeError"


def test_find_img_tags(configuration, crawler, empty_ignore_crawler, expectations):
    for url in expectations.keys():
        soup: BeautifulSoup = BeautifulSoup(crawler.get_content(url), 'html.parser')
        img_links: List[str] = crawler.find_img_tags(soup, url)
        assert list(img_links) == expectations[url]['img_links'], 'img_links must match expectations'
        img_links = list(empty_ignore_crawler.find_img_tags(soup, url))
        assert len(img_links) > 0, 'find_img_tags must support empty ignore'
        assert img_links[0].endswith('.png'), 'find_img_tags should have a match'


def test_download_file(crawler, mock_images):
    # for file in iglob(os.path.join(os.path.abspath('.'), 'output', '*')):
    #     os.remove(file)
    for url in mock_images.keys():
        file_path = crawler.download_file(url)
        assert file_path, "file_path must be returned"
        assert file_path == 'output/1ce559cc3fa5dfd70d914a3f083b357c474fdf63.jpg', "follows file path specification"
        with open(file_path, 'rb') as file:
            jpeg = file.read()
            assert len(jpeg) > 0, "file must have data"
            assert jpeg == mock_images[url]['content'], "file must match source content"
        assert crawler.download_file(url), "Increase branch coverage"


def test_follow_href(crawler, empty_follow_crawler):
    retval = crawler.follow_href('https://www.fbi.gov/wanted/ecap/unknown-individual-jane-doe-37')
    assert retval, "URL should test true"
    retval = crawler.follow_href('https://www.fbi.gov/wanted/vicap/unknown-individual-jane-doe-37')
    assert retval, "URL should test true"
    retval = empty_follow_crawler.follow_href('https://www.fbi.gov/wanted/vicap/unknown-individual-jane-doe-37')
    assert retval, "None follow_pattern should test true"

    retval = crawler.follow_href('https://www.fbi.gov/wanted/seeking-info/john-doe')
    assert not retval, "URL should test false"
    retval = crawler.follow_href('mailto:foo@bar.com')
    assert not retval, "mailto: should test false"


def test_find_a_tags(crawler: HtmlCrawler, expectations: dict):
    for url in expectations.keys():
        soup: BeautifulSoup = BeautifulSoup(crawler.get_content(url), 'html.parser')
        a_tags = crawler.find_a_tags(soup, url)
        assert expectations[url]['a_tags'] == list(a_tags), 'a_tags must match expectations'


def test_crawl(crawler: HtmlCrawler, expectations: dict):
    for url in expectations.keys():
        crawler._crawl(url)


def test_cached(crawler: HtmlCrawler):
    headers = {'Content-Type': 'image/jpeg', 'Content-Length': '23930'}
    metadata_file = 'output/1ce559cc3fa5dfd70d914a3f083b357c474fdf63-metadata.json'
    destination = 'output/1ce559cc3fa5dfd70d914a3f083b357c474fdf63.jpg'
    assert crawler.cached(headers, metadata_file, destination), "Expect cache hit"

    assert not crawler.cached(headers, metadata_file, f"{destination}.foo"), "Expect cache miss; destination not found"
    headers = {'Content-Type': 'image/unknown', 'Content-Length': '23930'}
    assert not crawler.cached(headers, metadata_file, destination), "Expect cache miss; Content-Type mismatch"
    headers = {'Content-Type': 'image/jpeg', 'Content-Length': '1337'}
    assert not crawler.cached(headers, metadata_file, destination), "Expect cache miss; Content-Length mismatch"
    headers = {'Content-Type': 'image/unknown', 'Content-Length': '23930'}
    assert not crawler.cached(headers, f"{metadata_file}.foo",
                              destination), "Expect cache miss; metadata_file not found"
