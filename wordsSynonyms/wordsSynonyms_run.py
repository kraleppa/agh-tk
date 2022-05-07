import Synonyms_receive_config, Synonyms_receive_connect

if __name__ == "__main__":
    serverconfigure = Synonyms_receive_config.RabbitMqServerConfigure(
        host = 'rabbitmq',
        queue='words.synonyms')

    logger = Synonyms_receive_config.RabbitMqServerConfigure.create_logger()

    server = Synonyms_receive_connect.RabbitmqServer(server=serverconfigure, logger=logger)
    logger.info('Server started waiting for Messages')
    server.startserver()