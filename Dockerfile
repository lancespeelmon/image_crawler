FROM python:3

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt
RUN mkdir ./output

CMD [ "python3", "./sync_crawler.py" ]
