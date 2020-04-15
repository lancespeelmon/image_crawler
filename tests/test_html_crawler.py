import os
from typing import List
from urllib.parse import quote

import pytest
from bs4 import BeautifulSoup

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
    return HtmlCrawler(logger)


@pytest.fixture
def expectations(requests_mock):
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
                          'https://www.fbi.gov/wanted/topten/jason-derek-brown/@@images/image/preview']
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
                          'https://www.interpol.int/bundles/interpolfront/images/logo-blanc.png']
        },
    }
    # mock page content
    for url in expectations.keys():
        filename = (os.path.join(os.path.dirname(__file__), 'fixtures', quote(url, '')))
        with open(filename, 'r') as file:
            content = file.read()
            assert len(content) > 0, "content mock must have data"
            expectations[url]['content'] = content.encode('utf-8')
            requests_mock.get(url, text=content)
    return expectations


@pytest.fixture
def mock_images(requests_mock):
    """ Loads the mock images from tests/fixtures/<image>
    """
    expectations = {}
    url = 'https://www.fbi.gov/wanted/topten/yaser-abdel-said/@@images/image/preview'
    filename = (os.path.join(os.path.dirname(__file__), 'fixtures', '1ce559cc3fa5dfd70d914a3f083b357c474fdf63.jpg'))
    with open(filename, 'rb') as file:
        jpeg = file.read()
        requests_mock.get(url, content=jpeg, headers={'content-type': 'image/jpeg'})
        expectations[url] = {}
        expectations[url]['content'] = jpeg
    return expectations


def test_init(logger, crawler):
    # happy path
    assert crawler, "crawler should not be None"
    assert crawler.logger() is logger, "logger should be same as assigned"

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


def test_find_img_tags(configuration, crawler, expectations):
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
    for url in expectations.keys():
        soup: BeautifulSoup = BeautifulSoup(crawler.get_content(url), 'html.parser')
        img_links: List[str] = crawler.find_img_tags(soup, url, ignore=image_ignore_patterns)
        assert len(img_links) > 0, "img_links length must be greater than 0"
        assert img_links == expectations[url]['img_links'], 'img_links must match expectations'


def test_download_file(crawler, mock_images):
    for url in mock_images.keys():
        file_path = crawler.download_file(url)
        assert file_path, "file_path must be returned"
        assert file_path == 'output/1ce559cc3fa5dfd70d914a3f083b357c474fdf63.jpg', "follows file path specification"
        with open(file_path, 'rb') as file:
            jpeg = file.read()
            assert len(jpeg) > 0, "file must have data"
            assert jpeg == mock_images[url]['content'], "file must match source content"
