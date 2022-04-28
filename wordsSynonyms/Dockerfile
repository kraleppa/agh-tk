FROM python:3

ADD Synonyms_receive.py /
ADD Synonyms_send.py /

RUN pip install --upgrade pip
RUN pip install pika

COPY thesaurus_full.txt ./

CMD [ "python", "./Synonyms_receive.py" ]