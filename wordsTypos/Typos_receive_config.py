import logging

class RabbitMqServerConfigure():

    def __init__(self, host, queue, passive, durable):

        """ Server configuration"""

        self.host = host
        self.queue = queue
        self.passive = passive
        self.durable = durable

    @staticmethod
    def create_logger():
        logger = logging.getLogger('wordsTyposInfo')
        logger.setLevel(logging.WARNING)
        return logger