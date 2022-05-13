import logging

class RabbitMqServerConfigure():

    def __init__(self, host, queue):

        """ Server configuration"""

        self.host = host
        self.queue = queue

    @staticmethod
    def create_logger(log_name):
        logging.basicConfig(format='%(asctime)s - %(name)s%(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S%p')
        logger = logging.getLogger(log_name)
        logger.setLevel(logging.INFO)
        return logger

