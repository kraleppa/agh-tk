import time
import pika
import json
import Forms_send_connect, Forms_receive_config

import morfeusz2

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
        my_words = []
        for word in message['phrase']:
            my_words.append(word)
        logger = Forms_receive_config.RabbitMqServerConfigure.create_logger()
        logger.info(f'Message received: {message}')
        logger.info(f'Words received: {my_words}')

        forms = RabbitmqServer.forms_generator(my_words)
        for form in forms:
            if form not in message['words']:
                message['words'].append(form)


        message["queueKey"] = message["filters"]["searchModes"][0]
        current_search_mode = message["filters"]["searchModes"][0]
        message["filters"]["searchModes"]. \
            append(message["filters"]["searchModes"].
                   pop(message["filters"]["searchModes"].
                       index(current_search_mode)))

        new_search_mode = message["queueKey"]

        rabbitmq = Forms_send_connect.RabbitMq.rabbit_send(message, new_search_mode)

        logger.info(f'The Message was forwarded to: {new_search_mode}')
        logger.info(f'Published Message: {message}')

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
