# Python Image Crawler

## Development Environment

While you _can_ use a global python environment, it is highly recommended you use
a virtual python environment located in the `.venv` directory; for example:

```
python3 -m venv .venv
source .venv/bin/activate
```

Next you can install the required python modules:

```
pip install -r requirements-dev.txt
```

## Running

```
❯ make run

LOG_LEVEL=DEBUG python3 ./sync_crawler.py
DEBUG|root|html_crawler.py:78|crawl| url = https://www.fbi.gov/wanted/topten
DEBUG|urllib3.connectionpool|connectionpool.py:959|_new_conn| Starting new HTTPS connection (1): www.fbi.gov:443
DEBUG|urllib3.connectionpool|connectionpool.py:437|_make_request| https://www.fbi.gov:443 "GET /wanted/topten HTTP/1.1" 200 None
DEBUG|root|fbi_crawler.py:24|find_img_tags| ignore hit: https://www.fbi.gov/++theme++fbigov.theme/images/fbibannerseal.png
DEBUG|urllib3.connectionpool|connectionpool.py:437|_make_request| https://www.fbi.gov:443 "GET /wanted/topten/alexis-flores/@@images/image/preview HTTP/1.1" 200 20915
INFO|root|html_crawler.py:50|download_file| write file: output/9bcfa6d7353d80d1a4db43955622e4135cc703de.jpg
DEBUG|urllib3.connectionpool|connectionpool.py:437|_make_request| https://www.fbi.gov:443 "GET /wanted/topten/eugene-palmer/@@images/image/preview HTTP/1.1" 200 29628
INFO|root|html_crawler.py:50|download_file| write file: output/b88fa1f8ab797e2adb1335a70de7e9e46ea17a8f.jpg
DEBUG|urllib3.connectionpool|connectionpool.py:437|_make_request| https://www.fbi.gov:443 "GET /wanted/topten/santiago-mederos/@@images/image/preview HTTP/1.1" 200 19301
INFO|root|html_crawler.py:50|download_file| write file: output/c4b76e8b33d9c7ff4027f0a2fbbf9054b6994e77.jpg
DEBUG|urllib3.connectionpool|connectionpool.py:437|_make_request| https://www.fbi.gov:443 "GET /wanted/topten/rafael-caro-quintero/@@images/image/preview HTTP/1.1" 200 23860
INFO|root|html_crawler.py:50|download_file| write file: output/c99ff44f6c21333afe797ed837b0f2da65360a7d.jpg
DEBUG|urllib3.connectionpool|connectionpool.py:437|_make_request| https://www.fbi.gov:443 "GET /wanted/topten/robert-william-fisher/@@images/image/preview HTTP/1.1" 200 19152
INFO|root|html_crawler.py:50|download_file| write file: output/3b81130672ff31e75e87833e2080c94b53ce017a.jpg
DEBUG|urllib3.connectionpool|connectionpool.py:437|_make_request| https://www.fbi.gov:443 "GET /wanted/topten/bhadreshkumar-chetanbhai-patel/@@images/image/preview HTTP/1.1" 200 21688
INFO|root|html_crawler.py:50|download_file| write file: output/90b650e12af3b3025946d9b7494e8f6163b20b48.jpg
DEBUG|urllib3.connectionpool|connectionpool.py:437|_make_request| https://www.fbi.gov:443 "GET /wanted/topten/alejandro-castillo/@@images/image/preview HTTP/1.1" 200 25003
INFO|root|html_crawler.py:50|download_file| write file: output/35076b490a4b65c5e357eae1c751c287db1dc53b.jpg
DEBUG|urllib3.connectionpool|connectionpool.py:437|_make_request| https://www.fbi.gov:443 "GET /wanted/topten/arnoldo-jimenez/@@images/image/preview HTTP/1.1" 200 132828
INFO|root|html_crawler.py:50|download_file| write file: output/e04bcbec3a5efc2c0f5ecb94fb9b6cb234da727e.png
DEBUG|urllib3.connectionpool|connectionpool.py:437|_make_request| https://www.fbi.gov:443 "GET /wanted/topten/yaser-abdel-said/@@images/image/preview HTTP/1.1" 200 23930
INFO|root|html_crawler.py:50|download_file| write file: output/1ce559cc3fa5dfd70d914a3f083b357c474fdf63.jpg
DEBUG|urllib3.connectionpool|connectionpool.py:437|_make_request| https://www.fbi.gov:443 "GET /wanted/topten/jason-derek-brown/@@images/image/preview HTTP/1.1" 200 22463
INFO|root|html_crawler.py:50|download_file| write file: output/44d6baf352ee1359610380c876b06d07272a5797.jpg
INFO|root|sync_crawler.py:17|worker| Downloaded 10 files
DEBUG|root|html_crawler.py:78|crawl| url = https://www.interpol.int/en/How-we-work/Notices/View-Red-Notices
DEBUG|urllib3.connectionpool|connectionpool.py:959|_new_conn| Starting new HTTPS connection (1): www.interpol.int:443
DEBUG|urllib3.connectionpool|connectionpool.py:437|_make_request| https://www.interpol.int:443 "GET /en/How-we-work/Notices/View-Red-Notices HTTP/1.1" 200 25939
DEBUG|urllib3.connectionpool|connectionpool.py:437|_make_request| https://www.interpol.int:443 "GET /bundles/interpolfront/images/logo.png HTTP/1.1" 200 5947
INFO|root|html_crawler.py:50|download_file| write file: output/4d8e5f9d00e3b2b45a11b9f667d9e1d244c3c723.png
DEBUG|urllib3.connectionpool|connectionpool.py:437|_make_request| https://www.interpol.int:443 "GET /bundles/interpolfront/images/logo-text-only.png HTTP/1.1" 200 3442
INFO|root|html_crawler.py:50|download_file| write file: output/f9c0b5eb4c75e42f16dc9a67e842aa6310373c7b.png
DEBUG|urllib3.connectionpool|connectionpool.py:437|_make_request| https://www.interpol.int:443 "GET /var/interpol/storage/images/1/1/1/6/76111-12-eng-GB/RedNoticeEnLR.jpg HTTP/1.1" 200 176039
INFO|root|html_crawler.py:50|download_file| write file: output/9bd91ed4cbfc0e45786b9d2f809c2722d7e62a5c.jpg
DEBUG|urllib3.connectionpool|connectionpool.py:437|_make_request| https://www.interpol.int:443 "GET /bundles/interpolfront/images/photo-not-available.png HTTP/1.1" 200 10210
INFO|root|html_crawler.py:50|download_file| write file: output/5f2396b722e4669a9bb1e16b0c9fe27f6e113bbe.png
DEBUG|urllib3.connectionpool|connectionpool.py:437|_make_request| https://www.interpol.int:443 "GET /bundles/interpolfront/images/rednotice.png HTTP/1.1" 200 1906
INFO|root|html_crawler.py:50|download_file| write file: output/916b3ba60fb51bbbb97bbd1b979a61af87d68a4e.png
DEBUG|urllib3.connectionpool|connectionpool.py:437|_make_request| https://www.interpol.int:443 "GET /bundles/interpolfront/images/rednotice_big.png HTTP/1.1" 200 27313
INFO|root|html_crawler.py:50|download_file| write file: output/cbb734c50f293077b69870da715b4cccd5676981.png
DEBUG|urllib3.connectionpool|connectionpool.py:437|_make_request| https://www.interpol.int:443 "GET /bundles/interpolfront/images/photo-not-available.png HTTP/1.1" 200 10210
INFO|root|html_crawler.py:50|download_file| write file: output/5f2396b722e4669a9bb1e16b0c9fe27f6e113bbe.png
DEBUG|urllib3.connectionpool|connectionpool.py:437|_make_request| https://www.interpol.int:443 "GET /bundles/interpolfront/images/rednotice.png HTTP/1.1" 200 1906
INFO|root|html_crawler.py:50|download_file| write file: output/916b3ba60fb51bbbb97bbd1b979a61af87d68a4e.png
DEBUG|urllib3.connectionpool|connectionpool.py:437|_make_request| https://www.interpol.int:443 "GET /bundles/interpolfront/images/logo-blanc.png HTTP/1.1" 200 5943
INFO|root|html_crawler.py:50|download_file| write file: output/e5669f1b53ef574c01a587848a44583cddb69507.png
INFO|root|sync_crawler.py:17|worker| Downloaded 9 files
INFO|root|sync_crawler.py:32|main| Elapsed time: 1.73

❯ file output/*
output/1ce559cc3fa5dfd70d914a3f083b357c474fdf63.jpg: JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, progressive, precision 8, 311x400, components 3
output/35076b490a4b65c5e357eae1c751c287db1dc53b.jpg: JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, progressive, precision 8, 323x400, components 3
output/3b81130672ff31e75e87833e2080c94b53ce017a.jpg: JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, progressive, precision 8, 300x400, components 3
output/44d6baf352ee1359610380c876b06d07272a5797.jpg: JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, progressive, precision 8, 367x400, components 3
output/4d8e5f9d00e3b2b45a11b9f667d9e1d244c3c723.png: PNG image data, 101 x 92, 8-bit/color RGBA, non-interlaced
output/5f2396b722e4669a9bb1e16b0c9fe27f6e113bbe.png: PNG image data, 190 x 145, 8-bit/color RGB, non-interlaced
output/90b650e12af3b3025946d9b7494e8f6163b20b48.jpg: JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, progressive, precision 8, 300x400, components 3
output/916b3ba60fb51bbbb97bbd1b979a61af87d68a4e.png: PNG image data, 26 x 40, 8-bit/color RGBA, non-interlaced
output/9bcfa6d7353d80d1a4db43955622e4135cc703de.jpg: JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, progressive, precision 8, 297x400, components 3
output/9bd91ed4cbfc0e45786b9d2f809c2722d7e62a5c.jpg: JPEG image data, Exif standard: [TIFF image data, big-endian, direntries=12, height=3649, bps=0, PhotometricIntepretation=RGB, orientation=upper-left, width=2433], progressive, precision 8, 433x650, components 3
output/b88fa1f8ab797e2adb1335a70de7e9e46ea17a8f.jpg: JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, progressive, precision 8, 292x400, components 3
output/c4b76e8b33d9c7ff4027f0a2fbbf9054b6994e77.jpg: JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, progressive, precision 8, 320x400, components 3
output/c99ff44f6c21333afe797ed837b0f2da65360a7d.jpg: JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, progressive, precision 8, 400x375, components 3
output/cbb734c50f293077b69870da715b4cccd5676981.png: PNG image data, 185 x 279, 8-bit/color RGBA, non-interlaced
output/e04bcbec3a5efc2c0f5ecb94fb9b6cb234da727e.png: PNG image data, 266 x 400, 8-bit/color RGB, non-interlaced
output/e5669f1b53ef574c01a587848a44583cddb69507.png: PNG image data, 101 x 92, 8-bit/color RGBA, non-interlaced
output/f9c0b5eb4c75e42f16dc9a67e842aa6310373c7b.png: PNG image data, 101 x 16, 8-bit/color RGBA, non-interlaced
```

## Test Coverage

All tests _must_ pass before a merge request will be accepted.

```
make test
```

If you are fixing a bug or adding a new feature, test coverage
should be included.

## Coding Standards

Apply all standard python coding style best practices.
The CICD pipeline _will_ fail if there are any issues.

```
make lint
make isort
```

## Running Locally

##### Python virtual environment

```
make run
```

##### Docker environment

```
make docker-build
make docker-run
```

## Cleaning House

```
make clean
make real-clean
```
