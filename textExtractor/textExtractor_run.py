import receive_config, receive_connect

if __name__ == "__main__":
    serverconfigure = receive_config.RabbitMqServerConfigure(
        host = 'rabbitmq',
        queue='format.txt',
        passive=True,
        durable=True)

    logger = receive_config.RabbitMqServerConfigure.create_logger()

    server = receive_connect.RabbitmqServer(server=serverconfigure, logger=logger)
    logger.warning('TextExtractor: Server started waiting for Messages')
    server.startserver()