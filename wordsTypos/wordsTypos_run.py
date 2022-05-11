import sys
import os

if __name__ == "__main__":

    dir = os.path.dirname(os.getcwd())
    sys.path.insert(1, dir)

    from wordsServices_textExtractor_config import receive_config, receive_connect, callback_config
    import Typos_functions

    log_name = "wordsTypos"
    exchange = 'words'
    host = 'localhost'
    queue = 'words.typos'
    function = Typos_functions.create_typos_list

    serverconfigure = receive_config.RabbitMqServerConfigure(
        host=host,
        queue=queue)

    logger = receive_config.RabbitMqServerConfigure.create_logger(log_name)

    server = receive_connect.RabbitmqServer(server=serverconfigure, logger=logger)
    logger.info('Server started waiting for Messages')
    callback = callback_config.Callback(log_name, exchange, host, function)
    server.startserver(callback= callback.callback)