import pika
import json
import os
import send

class RabbitMqServerConfigure():

    def __init__(self, host, queue, passive, durable):

        """ Server configuration"""

        self.host = host
        self.queue = queue
        self.passive = passive
        self.durable = durable

class RabbitmqServer():

    def __init__(self, server):

        """
        :param server: Object of class RabbitMqServerConfigure
        """

        self.server = server
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.server.host))
        self._channel = self._connection.channel()
        self._tem = self._channel.queue_declare(queue=self.server.queue,
                                                passive=self.server.passive,
                                                durable=self.server.durable)
        print("Server started waiting for Messages ")

    @staticmethod
    def callback(ch,method, properties, body):

        message = json.loads(body)
        myfile = message['file']

        extracted = RabbitmqServer.extract(myfile)
        message["text"] = extracted
        server = send.RabbitmqConfigure(
                        exchange='text',
                        passive=True,
                        exchange_type='direct',
                        durable = True)
        rabbitmq = send.RabbitMq(server, host_name='rabbitmq')
        rabbitmq.publish(message=message, routing_key='text')

    @staticmethod
    def extract(file):
        file = os.path.join(file)
        with open(file, 'r') as f:
            msg = f.read()
        return msg

    def startserver(self):
        self._channel.basic_consume(
            queue=self.server.queue,
            on_message_callback=RabbitmqServer.callback,
            auto_ack=True)
        self._channel.start_consuming()

if __name__ == "__main__":
    serverconfigure = RabbitMqServerConfigure(
                                            host = 'rabbitmq',
                                            queue='format.txt',
                                            passive=True,
                                            durable=True)

    server = RabbitmqServer(server=serverconfigure)
    server.startserver()
