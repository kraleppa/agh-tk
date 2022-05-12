import sys
import os

def run_app(log_name, exchange, host, queue, function):

    dir = os.path.dirname(os.getcwd())
    sys.path.insert(1, dir)

    from wordsServices_textExtractor_config import receive_config, receive_connect, callback_config

    serverconfigure = receive_config.RabbitMqServerConfigure(
        host = host,
        queue = queue)

    logger = receive_config.RabbitMqServerConfigure.create_logger(log_name)

    server = receive_connect.RabbitmqServer(server=serverconfigure, logger=logger)
    logger.info('Server started waiting for Messages')
    callback = callback_config.Callback(log_name, exchange, host, function)
    server.startserver(callback= callback.callback)