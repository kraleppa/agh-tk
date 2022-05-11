import json
import os
import sys

class Callback():

    def __init__(self, log_name, exchange, routing_key, host):

        self.log_name = log_name
        self.exchange = exchange
        self.host = host
        self.routing_key = routing_key

    def callback(self, ch,method, properties, body):

        dir = os.path.dirname(os.getcwd())
        sys.path.insert(1, dir)

        from wordsServices_textExtractor_config import receive_config, send_connect

        message = json.loads(body)
        myfile = message['file']
        logger = receive_config.RabbitMqServerConfigure.create_logger(self.log_name)
        logger.info(f'Received file: {myfile}')
        extracted = Callback.extract(myfile)
        message["text"] = extracted

        send_connect.RabbitMq.rabbit_send(message, self.host, self.routing_key, self.exchange)
        logger.info(f'Published Message: {message}')

    @staticmethod
    def extract(file):
        file = os.path.join(file)
        with open(file, 'r') as f:
            msg = f.read()
        return msg
