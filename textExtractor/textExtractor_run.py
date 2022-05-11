import sys
import os

if __name__ == "__main__":

    dir = os.path.dirname(os.getcwd())
    sys.path.insert(1, dir)

    from wordsServices_textExtractor_config import receive_config, receive_connect
    import Extractor_callback

    log_name = "textExtractor"
    exchange = 'text'
    routing_key = 'text'
    host = 'localhost'
    queue = 'format.txt'


    serverconfigure = receive_config.RabbitMqServerConfigure(
        host = host,
        queue = queue)

    logger = receive_config.RabbitMqServerConfigure.create_logger(log_name)

    server = receive_connect.RabbitmqServer(server=serverconfigure, logger=logger)
    logger.info('Server started waiting for Messages')
    callback = Extractor_callback.Callback(log_name, exchange, routing_key, host)
    server.startserver(callback= callback.callback)