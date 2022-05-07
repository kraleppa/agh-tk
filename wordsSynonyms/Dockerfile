FROM python:3

RUN mkdir -p /wordSynonyms

WORKDIR /wordSynonyms
COPY . .

RUN pip install pika

CMD [ "python", "wordsSynonyms_run.py" ]