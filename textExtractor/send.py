import pika
import json

class RabbitmqConfigure():

    def __init__(self, exchange, passive, exchange_type, durable):
        """ Configure Rabbit Mq Server  """
        self.exchange = exchange
        self.passive = passive
        self.exchange_type = exchange_type
        self.durable = durable

class RabbitMq():

    def __init__(self, server, host_name):

        self.server = server

        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host_name))
        self._channel = self._connection.channel()
        self._channel.exchange_declare(
            exchange=self.server.exchange,
            passive=self.server.passive,
            exchange_type=self.server.exchange_type,
            durable=self.server.durable
        )

    def publish(self, message, routing_key):

        self._channel.basic_publish(exchange=self.server.exchange,
                      routing_key=routing_key,
                      body=json.dumps(message))

        print(f"Published Message: {message}")
        self._connection.close()



