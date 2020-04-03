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
❯ python ./fbi_crawler.py

found title:    Ten Most Wanted Fugitives — FBI
download_image: https://www.fbi.gov/wanted/topten/alexis-flores/@@images/image/preview
download_image: https://www.fbi.gov/wanted/topten/eugene-palmer/@@images/image/preview
download_image: https://www.fbi.gov/wanted/topten/santiago-mederos/@@images/image/preview
download_image: https://www.fbi.gov/wanted/topten/rafael-caro-quintero/@@images/image/preview
download_image: https://www.fbi.gov/wanted/topten/robert-william-fisher/@@images/image/preview
download_image: https://www.fbi.gov/wanted/topten/bhadreshkumar-chetanbhai-patel/@@images/image/preview
download_image: https://www.fbi.gov/wanted/topten/alejandro-castillo/@@images/image/preview
download_image: https://www.fbi.gov/wanted/topten/arnoldo-jimenez/@@images/image/preview
download_image: https://www.fbi.gov/wanted/topten/yaser-abdel-said/@@images/image/preview
download_image: https://www.fbi.gov/wanted/topten/jason-derek-brown/@@images/image/preview

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
