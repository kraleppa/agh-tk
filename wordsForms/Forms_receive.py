import time
import pika
import json
import Forms_send
import logging
import morfeusz2

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
        flag = 0
        while flag == 0:
            try:
                self._connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.server.host))
                self._channel = self._connection.channel()
                self._channel.queue_declare(queue=self.server.queue,
                                            passive=self.server.passive,
                                            durable=self.server.durable)
                logger.warning('wordsForms: Connected to channel')
                flag = 1
            except:
                logger.warning('wordsForms: Cannot connect to channel - retrying in 5 seconds...')
                time.sleep(5.0)


    @staticmethod
    def callback(ch,method, properties, body):

        message = json.loads(body)
        my_words = message['words']
        logger.warning(f'wordsForms: Message received: {my_words}')

        forms = RabbitmqServer.forms_generator(my_words)
        message['words'] = forms

        rabbitmq = Forms_send.RabbitMq.rabbit_send(message)
        logger.warning(f'wordsForms: Published Message: {message}')

    def startserver(self):
        self._channel.basic_consume(
            queue=self.server.queue,
            on_message_callback=RabbitmqServer.callback,
            auto_ack=True)
        self._channel.start_consuming()

    @staticmethod
    def forms_generator(words):

        morf = morfeusz2.Morfeusz()
        forms = []
        for word in words:
            generated = morf.generate(word)
            for gen in generated:
                form = gen[0]
                if form not in forms:
                    forms.append(form)
        return forms

if __name__ == "__main__":
    logger = logging.getLogger('wordsFormsInfo')
    logger.setLevel(logging.WARNING)

    serverconfigure = RabbitMqServerConfigure(
        host = 'rabbitmq',
        queue='words.forms',
        passive=True,
        durable=True)

    server = RabbitmqServer(server=serverconfigure)
    logger.warning('wordsForms: Server started waiting for Messages')
    server.startserver()
