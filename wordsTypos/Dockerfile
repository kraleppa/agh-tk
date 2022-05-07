FROM python:3

RUN mkdir -p /wordTypos

WORKDIR /wordTypos
COPY . .

RUN pip install pika

CMD [ "python", "wordsTypos_run.py" ]