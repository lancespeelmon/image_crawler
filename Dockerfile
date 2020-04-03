FROM python:3

WORKDIR /app

ADD requirements.txt ./
ADD fbi_crawler.py ./

RUN pip install -r requirements.txt
RUN mkdir ./output

CMD [ "python", "./fbi_crawler.py" ]
