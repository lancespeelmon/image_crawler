#!/usr/bin/env python3

import logging
import mimetypes
import re
import requests
import uuid
from typing import List
from bs4 import BeautifulSoup


def find_img_tags(soup: BeautifulSoup):
    ''' Find most wanted images from fbi.gov website. '''

    hits: List[str] = []
    for img in soup.find_all('img'):
        src: str = img.get('src')
        if "/wanted/" in src:
            hits.append(src)
    return hits


def guess_extension(content_type: str):
    ''' Guess the file extension based on MIME content-type '''

    return mimetypes.guess_extension(content_type)


def download_image(url: str):
    ''' Downloand an image file from a URL '''

    print(f"download_image: {url}")
    regex = '''https://www.fbi.gov/wanted/topten/([0-9A-Za-z-]+)/@@images/image/preview'''
    filename: str = None
    match = re.search(regex, url)
    if match:
        filename = match.group(1)
    else:
        LOGGER.debug("Could not determine filename", url)
        filename = str(uuid.uuid4())
    try:
        r = requests.get(url, allow_redirects=True)
        ext = guess_extension(r.headers.get('content-type'))
        filename = f"{filename}{ext}"
        file = open(f"output/{filename}", 'wb')
        file.write(r.content)
        file.close()
    except Exception as e:
        LOGGER.error(f"error downloading: {filename}", e)


LOGGER = logging.getLogger(__file__)
LOGGER.setLevel(logging.DEBUG)

mimetypes.init()

URL = 'https://www.fbi.gov/wanted/topten'
PAGE = requests.get(URL)

SOUP: BeautifulSoup = BeautifulSoup(PAGE.content, 'html.parser')

# print(soup.prettify())

print(f"found title:    {SOUP.title.string}")

IMG_LINKS = find_img_tags(SOUP)
for url in IMG_LINKS:
    download_image(url)
