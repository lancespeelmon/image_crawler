FROM python:3

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt
RUN mkdir ./output

CMD [ "python", "./fbi_crawler.py" ]
