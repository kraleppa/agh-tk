FROM python:3

RUN mkdir -p /wordsServices_textExtractor_config

COPY ../wordsServices_textExtractor_config ./wordsServices_textExtractor_config

RUN mkdir -p /wordSynonyms

WORKDIR /wordSynonyms

COPY . .

RUN pip install pika

CMD [ "python", "wordsSynonyms_run.py" ]