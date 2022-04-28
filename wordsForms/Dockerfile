FROM python:3

ADD Forms_receive.py /
ADD Forms_send.py /

RUN pip install --upgrade pip
RUN pip install pika
RUN pip install morfeusz2

CMD [ "python", "./Forms_receive.py" ]