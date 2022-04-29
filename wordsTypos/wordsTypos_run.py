import Typos_receive_connect, Typos_receive_config

if __name__ == "__main__":

    serverconfigure = Typos_receive_config.RabbitMqServerConfigure(
        host = 'rabbitmq',
        queue='words.typos',
        passive=True,
        durable=True)

    logger = Typos_receive_config.RabbitMqServerConfigure.create_logger()

    server = Typos_receive_connect.RabbitmqServer(server=serverconfigure, logger=logger)
    logger.warning('wordsTypos: Server started waiting for Messages')
    server.startserver()