FROM python:3

RUN mkdir -p /wordsServices_textExtractor_config

COPY ./wordsServices_textExtractor_config ./wordsServices_textExtractor_config

RUN mkdir -p /wordsTypos

WORKDIR /wordsTypos

COPY ./wordsTypos .

RUN pip install pika

CMD [ "python", "wordsTypos_run.py" ]