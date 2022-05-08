import receive_config, receive_connect

if __name__ == "__main__":
    serverconfigure = receive_config.RabbitMqServerConfigure(
        host = 'rabbitmq',
        queue='format.txt')

    logger = receive_config.RabbitMqServerConfigure.create_logger()

    server = receive_connect.RabbitmqServer(server=serverconfigure, logger=logger)
    logger.info('Server started waiting for Messages')
    server.startserver()