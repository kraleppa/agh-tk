class RabbitmqConfigure():

    def __init__(self, host, exchange,routing_key, content_encoding):
        """ Configure Rabbit Mq Server  """
        self.host = host
        self.exchange = exchange
        self.routing_key = routing_key
        self.content_encoding = content_encoding