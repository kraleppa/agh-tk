FROM python:3

RUN mkdir -p /wordsForms

WORKDIR /wordsForms
COPY . .

RUN pip install pika
RUN pip install morfeusz2

CMD [ "python", "wordForms_run.py" ]