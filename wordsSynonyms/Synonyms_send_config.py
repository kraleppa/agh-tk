class RabbitmqConfigure():

    def __init__(self, host, exchange, passive, exchange_type, durable, routing_key, content_encoding):
        """ Configure Rabbit Mq Server  """
        self.host = host
        self.exchange = exchange
        self.passive = passive
        self.exchange_type = exchange_type
        self.durable = durable
        self.routing_key = routing_key
        self.content_encoding = content_encoding