FROM python:3

RUN mkdir -p /wordForms

WORKDIR /wordForms
COPY . .

RUN pip install pika
RUN pip install morfeusz2

CMD [ "python", "wordForms_run.py" ]