import sys
import os
import json

class Callback():

    def __init__(self, log_name, exchange, host, function):

        self.log_name = log_name
        self.exchange = exchange
        self.host = host
        self.function = function

    def callback(self, ch,method, properties, body):

        dir = os.path.dirname(os.getcwd())
        sys.path.insert(1, dir)

        from wordsServices_textExtractor_config import receive_config, send_connect

        message = json.loads(body)
        my_words = message['phrase'].split()
        logger = receive_config.RabbitMqServerConfigure.create_logger(self.log_name)

        logger.info(f'Message received: {message}')
        logger.info(f'Words received: {my_words}')

        results = self.function(my_words)
        for res in results:
            if res not in message['words']:
                message['words'].append(res)

        queueKey = message["filters"]["searchModes"][0]
        message["filters"]["searchModes"].pop(0)
        message["filters"]["searchModes"].append(queueKey)

        new_search_mode = "words." + message["filters"]["searchModes"][0]

        send_connect.RabbitMq.rabbit_send(message, self.host, new_search_mode, self.exchange)

        logger.info(f'The Message was forwarded to: {new_search_mode}')
        logger.info(f'Published Message: {message}')
