import time
import pika
import json
import Synonyms_send_connect, Synonyms_receive_config

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
                self._channel.queue_declare(queue=self.server.queue,
                                            passive=self.server.passive,
                                            durable=self.server.durable)
                logger.warning('wordsSynonyms: Connected to channel')
                flag = 1
            except:
                logger.warning('wordsSynonyms: Cannot connect to channel - retrying in 5 seconds...')
                time.sleep(5.0)


    @staticmethod
    def callback(ch,method, properties, body):

        message = json.loads(body)
        my_words = []
        for word in message['phrase']:
            my_words.append(word)
        logger = Synonyms_receive_config.RabbitMqServerConfigure.create_logger()
        logger.warning(f'wordsSynonyms: Message received: {message}')
        logger.warning(f'wordsSynonyms: Words received: {my_words}')

        synonyms = RabbitmqServer.find_synonyms(my_words)
        for syno in synonyms:
            message['words'].append(syno)

        rabbitmq = Synonyms_send_connect.RabbitMq.rabbit_send(message)
        logger.warning(f'wordsSynonyms: Published Message: {message}')

    def startserver(self):
        self._channel.basic_consume(
            queue=self.server.queue,
            on_message_callback=RabbitmqServer.callback,
            auto_ack=True)
        self._channel.start_consuming()

    @staticmethod
    def find_synonyms(words):
        global_synonyms = []
        for word in words:
            local_synonyms = []
            word = word.lower()
            with open('thesaurus_full.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    dict_word = line.split(';')
                    if dict_word[0] == word:
                        local_synonyms.append(dict_word)
            synonyms = [item for sublist in local_synonyms for item in sublist]
            local_synonyms = RabbitmqServer.words_filter(synonyms)
            for local in local_synonyms:
                global_synonyms.append(local)
        for glo in global_synonyms:
            words.append(glo)
        return words

    @staticmethod
    def words_filter(syn):
        syn = [word.strip() for word in syn]
        syn = [syn.remove(word) if ' ' in word else word for word in syn]
        syn = [word for word in syn if word is not None]
        return syn