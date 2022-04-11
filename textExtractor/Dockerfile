FROM python:3

ADD receive.py /
ADD send.py /

RUN pip install --upgrade pip
RUN pip install pika

COPY test.txt ./

CMD [ "python", "./receive.py" ]