FROM rabbitmq:3-management

COPY rabbitmq.conf /etc/rabbitmq/
COPY definitions.json /etc/rabbitmq/

RUN apt-get update
RUN apt-get install -y curl