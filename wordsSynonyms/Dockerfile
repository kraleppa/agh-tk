FROM python:3

RUN mkdir -p /wordsServices_textExtractor_config

COPY ./wordsServices_textExtractor_config ./wordsServices_textExtractor_config

RUN mkdir -p /wordsSynonyms

WORKDIR /wordsSynonyms

COPY ./wordsSynonyms .

RUN pip install pika

CMD [ "python", "wordsSynonyms_run.py" ]