import sys
import os

if __name__ == "__main__":

    dir = os.path.dirname(os.getcwd())
    sys.path.insert(1, dir)

    from wordsServices_textExtractor_config import receive_config, receive_connect
    from converter_callback import ConverterCallback

    log_name = "converter"
    exchange = "words"
    routing_key = "scraper"
    host = "rabbitmq"
    queue = "format.audio.mp3"

    serverconfigure = receive_config.RabbitMqServerConfigure(
        host=host,
        queue=queue
    )

    logger = receive_config.RabbitMqServerConfigure.create_logger(log_name)

    server = receive_connect.RabbitmqServer(server=serverconfigure, logger=logger)
    logger.info("Server started waiting for Messages")
    callback = ConverterCallback(log_name, exchange, routing_key, host)
    server.startserver(callback=callback.callback)
