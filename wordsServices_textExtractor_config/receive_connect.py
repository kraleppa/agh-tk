import time
import pika


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

    def startserver(self, callback):
        self._channel.basic_consume(
            queue=self.server.queue,
            on_message_callback=callback,
            auto_ack=True)
        self._channel.start_consuming()
