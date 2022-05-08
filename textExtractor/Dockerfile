FROM python:3

RUN mkdir -p /textExtractor

WORKDIR /textExtractor
COPY . .

RUN pip install pika


CMD [ "python", "textExtractor_run.py" ]