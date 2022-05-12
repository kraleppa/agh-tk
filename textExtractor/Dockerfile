FROM python:3

RUN mkdir -p /wordsServices_textExtractor_config

COPY ./wordsServices_textExtractor_config ./wordsServices_textExtractor_config

RUN mkdir -p /textExtractor

WORKDIR /textExtractor

COPY ./textExtractor .

RUN pip install pika


CMD [ "python", "textExtractor_run.py" ]