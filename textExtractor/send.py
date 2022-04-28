import pika
import json

class RabbitmqConfigure():

    def __init__(self, host, exchange, passive, exchange_type, durable, routing_key, content_encoding):
        """ Configure Rabbit Mq Server  """
        self.host = host
        self.exchange = exchange
        self.passive = passive
        self.exchange_type = exchange_type
        self.durable = durable
        self.routing_key = routing_key
        self.content_encoding = content_encoding

class RabbitMq():

    def __init__(self, server):

        self.server = server

        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.server.host))
        self._channel = self._connection.channel()
        self._content_encoding = self.server.content_encoding
        self._routing_key = self.server.routing_key
        self._channel.exchange_declare(
            exchange=self.server.exchange,
            passive=self.server.passive,
            exchange_type=self.server.exchange_type,
            durable=self.server.durable
        )

    def publish(self, message):

        _properties = pika.BasicProperties(content_encoding=self.server.content_encoding)
        self._channel.basic_publish(exchange=self.server.exchange,
                                    routing_key=self.server.routing_key,
                                    body=json.dumps(message),
                                    properties=_properties
                                    )

        self._connection.close()

    @staticmethod
    def rabbit_send(msg):
        server = RabbitmqConfigure(
            host='rabbitmq',
            exchange='text',
            passive=True,
            exchange_type='direct',
            durable=True,
            routing_key='text',
            content_encoding='utf-8'
        )
        rabbitmq = RabbitMq(server)
        message = msg
        rabbitmq.publish(message=message)



