# FBI Most Wanted Crawler

## Python Development Environment

While you can use a global python environment, it is highly suggested you use
a virtual python environment located in the `.venv` directory; for example:

```
python3 -m venv .venv
source .venv/bin/activate
```

Next you can install the required python modules:

```
pip install -r requirements.txt
```

## Running

```
❯ LOG_LEVEL=DEBUG python ./fbi_crawler.py

DEBUG|urllib3.connectionpool|connectionpool.py:959|_new_conn| Starting new HTTPS connection (1): www.fbi.gov:443
DEBUG|urllib3.connectionpool|connectionpool.py:437|_make_request| https://www.fbi.gov:443 "GET /wanted/topten HTTP/1.1" 200 None
INFO|root|fbi_crawler.py:64|<module>| found title: Ten Most Wanted Fugitives — FBI
DEBUG|root|fbi_crawler.py:20|find_img_tags| add hit: https://www.fbi.gov/wanted/topten/alexis-flores/@@images/image/preview
DEBUG|root|fbi_crawler.py:20|find_img_tags| add hit: https://www.fbi.gov/wanted/topten/eugene-palmer/@@images/image/preview
DEBUG|root|fbi_crawler.py:20|find_img_tags| add hit: https://www.fbi.gov/wanted/topten/santiago-mederos/@@images/image/preview
DEBUG|root|fbi_crawler.py:20|find_img_tags| add hit: https://www.fbi.gov/wanted/topten/rafael-caro-quintero/@@images/image/preview
DEBUG|root|fbi_crawler.py:20|find_img_tags| add hit: https://www.fbi.gov/wanted/topten/robert-william-fisher/@@images/image/preview
DEBUG|root|fbi_crawler.py:20|find_img_tags| add hit: https://www.fbi.gov/wanted/topten/bhadreshkumar-chetanbhai-patel/@@images/image/preview
DEBUG|root|fbi_crawler.py:20|find_img_tags| add hit: https://www.fbi.gov/wanted/topten/alejandro-castillo/@@images/image/preview
DEBUG|root|fbi_crawler.py:20|find_img_tags| add hit: https://www.fbi.gov/wanted/topten/arnoldo-jimenez/@@images/image/preview
DEBUG|root|fbi_crawler.py:20|find_img_tags| add hit: https://www.fbi.gov/wanted/topten/yaser-abdel-said/@@images/image/preview
DEBUG|root|fbi_crawler.py:20|find_img_tags| add hit: https://www.fbi.gov/wanted/topten/jason-derek-brown/@@images/image/preview
DEBUG|urllib3.connectionpool|connectionpool.py:437|_make_request| https://www.fbi.gov:443 "GET /wanted/topten/alexis-flores/@@images/image/preview HTTP/1.1" 200 20915
INFO|root|fbi_crawler.py:45|download_image| write file: output/alexis-flores.jpg
DEBUG|urllib3.connectionpool|connectionpool.py:437|_make_request| https://www.fbi.gov:443 "GET /wanted/topten/eugene-palmer/@@images/image/preview HTTP/1.1" 200 29628
INFO|root|fbi_crawler.py:45|download_image| write file: output/eugene-palmer.jpg
DEBUG|urllib3.connectionpool|connectionpool.py:437|_make_request| https://www.fbi.gov:443 "GET /wanted/topten/santiago-mederos/@@images/image/preview HTTP/1.1" 200 19301
INFO|root|fbi_crawler.py:45|download_image| write file: output/santiago-mederos.jpg
DEBUG|urllib3.connectionpool|connectionpool.py:437|_make_request| https://www.fbi.gov:443 "GET /wanted/topten/rafael-caro-quintero/@@images/image/preview HTTP/1.1" 200 23860
INFO|root|fbi_crawler.py:45|download_image| write file: output/rafael-caro-quintero.jpg
DEBUG|urllib3.connectionpool|connectionpool.py:437|_make_request| https://www.fbi.gov:443 "GET /wanted/topten/robert-william-fisher/@@images/image/preview HTTP/1.1" 200 19152
INFO|root|fbi_crawler.py:45|download_image| write file: output/robert-william-fisher.jpg
DEBUG|urllib3.connectionpool|connectionpool.py:437|_make_request| https://www.fbi.gov:443 "GET /wanted/topten/bhadreshkumar-chetanbhai-patel/@@images/image/preview HTTP/1.1" 200 21688
INFO|root|fbi_crawler.py:45|download_image| write file: output/bhadreshkumar-chetanbhai-patel.jpg
DEBUG|urllib3.connectionpool|connectionpool.py:437|_make_request| https://www.fbi.gov:443 "GET /wanted/topten/alejandro-castillo/@@images/image/preview HTTP/1.1" 200 25003
INFO|root|fbi_crawler.py:45|download_image| write file: output/alejandro-castillo.jpg
DEBUG|urllib3.connectionpool|connectionpool.py:437|_make_request| https://www.fbi.gov:443 "GET /wanted/topten/arnoldo-jimenez/@@images/image/preview HTTP/1.1" 200 132828
INFO|root|fbi_crawler.py:45|download_image| write file: output/arnoldo-jimenez.png
DEBUG|urllib3.connectionpool|connectionpool.py:437|_make_request| https://www.fbi.gov:443 "GET /wanted/topten/yaser-abdel-said/@@images/image/preview HTTP/1.1" 200 23930
INFO|root|fbi_crawler.py:45|download_image| write file: output/yaser-abdel-said.jpg
DEBUG|urllib3.connectionpool|connectionpool.py:437|_make_request| https://www.fbi.gov:443 "GET /wanted/topten/jason-derek-brown/@@images/image/preview HTTP/1.1" 200 22463
INFO|root|fbi_crawler.py:45|download_image| write file: output/jason-derek-brown.jpg

❯ file output/*
output/alejandro-castillo.jpg:             JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, progressive, precision 8, 323x400, components 3
output/alexis-flores.jpg:                  JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, progressive, precision 8, 297x400, components 3
output/arnoldo-jimenez.png:                PNG image data, 266 x 400, 8-bit/color RGB, non-interlaced
output/bhadreshkumar-chetanbhai-patel.jpg: JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, progressive, precision 8, 300x400, components 3
output/eugene-palmer.jpg:                  JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, progressive, precision 8, 292x400, components 3
output/jason-derek-brown.jpg:              JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, progressive, precision 8, 367x400, components 3
output/rafael-caro-quintero.jpg:           JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, progressive, precision 8, 400x375, components 3
output/robert-william-fisher.jpg:          JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, progressive, precision 8, 300x400, components 3
output/santiago-mederos.jpg:               JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, progressive, precision 8, 320x400, components 3
output/yaser-abdel-said.jpg:               JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, progressive, precision 8, 311x400, components 3
```
