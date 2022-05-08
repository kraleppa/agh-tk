import Forms_receive_config, Forms_receive_connect

if __name__ == "__main__":
    serverconfigure = Forms_receive_config.RabbitMqServerConfigure(
        host = 'rabbitmq',
        queue='words.forms')

    logger = Forms_receive_config.RabbitMqServerConfigure.create_logger()

    server = Forms_receive_connect.RabbitmqServer(server=serverconfigure, logger=logger)
    logger.info('Server started waiting for Messages')
    server.startserver()