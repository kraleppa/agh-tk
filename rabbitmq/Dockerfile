FROM rabbitmq:3-management

COPY rabbitmq.conf /etc/rabbitmq/
COPY definitions.json /etc/rabbitmq/

RUN rabbitmq-plugins enable rabbitmq_web_stomp
RUN apt-get update
RUN apt-get install -y curl