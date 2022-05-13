FROM python:3

RUN mkdir -p /wordsServices_textExtractor_config

COPY ./wordsServices_textExtractor_config ./wordsServices_textExtractor_config

RUN mkdir -p /wordsForms

WORKDIR /wordsForms

COPY ./wordsForms .

RUN pip install pika
RUN pip install morfeusz2

CMD [ "python", "wordForms_run.py" ]