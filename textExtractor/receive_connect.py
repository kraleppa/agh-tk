import time
import pika
import json
import os
import receive_config, send_connect


class RabbitmqServer():

    def __init__(self, server, logger):

        """
        :param server: Object of class RabbitMqServerConfigure
        """

        self.server = server
        self.logger = logger
        flag = 0
        while flag == 0:
            try:
                self._connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.server.host))
                self._channel = self._connection.channel()

                logger.info('Connected to channel')
                flag = 1
            except:
                logger.warning('Cannot connect to channel - retrying in 5 seconds...')
                time.sleep(5.0)

    @staticmethod
    def callback(ch,method, properties, body):
        message = json.loads(body)
        myfile = message['file']
        logger = receive_config.RabbitMqServerConfigure.create_logger()
        logger.info(f'Received file: {myfile}')
        extracted = RabbitmqServer.extract(myfile)
        message["text"] = extracted

        rabbitmq = send_connect.RabbitMq.rabbit_send(message)
        logger.info(f'Published Message: {message}')

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