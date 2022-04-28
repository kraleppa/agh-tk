import time
import pika
import json
import Synonyms_send
import logging

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
                logger.warning('wordsSynonyms: Connected to channel')
                flag = 1
            except:
                logger.warning('wordsSynonyms: Cannot connect to channel - retrying in 5 seconds...')
                time.sleep(5.0)


    @staticmethod
    def callback(ch,method, properties, body):

        message = json.loads(body)
        my_words = message['words']
        logger.warning(f'wordsSynonyms: Message received: {my_words}')

        synonyms = RabbitmqServer.find_synonyms(my_words)
        message['words'] = synonyms

        rabbitmq = Synonyms_send.RabbitMq.rabbit_send(message)
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
                        local_synonyms.append(dict_word[1:10])
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
        if len(syn) >= 5:
            syn = syn[0:5]
        return syn

if __name__ == "__main__":
    logger = logging.getLogger('wordsSynonymsInfo')
    logger.setLevel(logging.WARNING)

    serverconfigure = RabbitMqServerConfigure(
        host = 'rabbitmq',
        queue='words.synonyms',
        passive=True,
        durable=True)

    server = RabbitmqServer(server=serverconfigure)
    logger.warning('wordsSynonyms: Server started waiting for Messages')
    server.startserver()
