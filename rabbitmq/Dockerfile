FROM rabbitmq:3-management

RUN apt-get update
RUN apt-get install -y curl

COPY rabbitmq.conf /etc/rabbitmq/
COPY definitions.json /etc/rabbitmq/

RUN rabbitmq-plugins enable rabbitmq_web_stomp
