import sys
import os

log_name = "audio_service"
exchange = "text"
routing_key = "text"
host = "rabbitmq"
queue = "format.audio"

if __name__ == "__main__":

    dir = os.path.dirname(os.getcwd())
    sys.path.insert(1, dir)

    from wordsServices_textExtractor_config import receive_config, receive_connect
    from audio_extractor_callback import AudioExtractorCallback

    serverconfigure = receive_config.RabbitMqServerConfigure(
        host=host,
        queue=queue
    )

    logger = receive_config.RabbitMqServerConfigure.create_logger(log_name)

    server = receive_connect.RabbitmqServer(server=serverconfigure, logger=logger)
    logger.info("Server started waiting for Messages")
    callback = AudioExtractorCallback(log_name, exchange, routing_key, host)
    server.startserver(callback=callback.callback)
