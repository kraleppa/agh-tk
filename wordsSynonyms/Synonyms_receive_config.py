import logging

class RabbitMqServerConfigure():

    def __init__(self, host, queue):

        """ Server configuration"""

        self.host = host
        self.queue = queue

    @staticmethod
    def create_logger():
        logging.basicConfig(format='%(asctime)s - %(name)s%(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S%p')
        logger = logging.getLogger('wordsSynonyms')
        logger.setLevel(logging.INFO)
        return logger

