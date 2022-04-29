import time
import pika
import json
import Typos_send_connect, Typos_receive_config
import random

class RabbitmqServer():

    def __init__(self, server, logger):

        """
        :param server: Object of class RabbitMqServerConfigure
        """

        self.server = server
        self.logger = logger
        flag = 0
        while flag == 0:
            try:
                self._connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.server.host))
                self._channel = self._connection.channel()
                self._channel.queue_declare(queue=self.server.queue,
                                            passive=self.server.passive,
                                            durable=self.server.durable)
                logger.warning('wordsTypos: Connected to channel')
                flag = 1
            except:
                logger.warning('wordsTypos: Cannot connect to channel - retrying in 5 seconds...')
                time.sleep(5.0)


    @staticmethod
    def callback(ch,method, properties, body):

        message = json.loads(body)
        my_words = message['words']
        logger = Typos_receive_config.RabbitMqServerConfigure.create_logger()
        logger.warning(f'wordsTypos: Message received: {my_words}')

        typos = RabbitmqServer.create_typos_list(my_words)
        message['words'] = typos

        rabbitmq = Typos_send_connect.RabbitMq.rabbit_send(message)
        logger.warning(f'wordsTypos: Published Message: {message}')

    def startserver(self):
        self._channel.basic_consume(
            queue=self.server.queue,
            on_message_callback=RabbitmqServer.callback,
            auto_ack=True)
        self._channel.start_consuming()

    @staticmethod
    def generate_typos(word, prob=0.05):
        keyApprox = {}
        keyApprox['q'] = "qwasedzx"
        keyApprox['w'] = "wqesadrfcx"
        keyApprox['e'] = "eęwrsfdqazxcvgt"
        keyApprox['r'] = "retdgfwsxcvgt"
        keyApprox['t'] = "tryfhgedcvbnju"
        keyApprox['y'] = "ytugjhrfvbnji"
        keyApprox['u'] = "uóyihkjtgbnmlo"
        keyApprox['i'] = "iuojlkyhnmlp"
        keyApprox['o'] = "oóipklujm"
        keyApprox['p'] = "plo['ik"

        keyApprox['a'] = "aąqszwxwdce"
        keyApprox['s'] = "sśwxadrfv"
        keyApprox['d'] = "decsfaqgbv"
        keyApprox['f'] = "fdgrvwsxyhn"
        keyApprox['g'] = "gtbfhedcyjn"
        keyApprox['h'] = "hyngjfrvkim"
        keyApprox['j'] = "jhknugtblom"
        keyApprox['k'] = "kjlinyhn"
        keyApprox['l'] = "lłokmpujn"

        keyApprox['z'] = "zźaxsvde"
        keyApprox['x'] = "xzcsdbvfrewq"
        keyApprox['c'] = "cćxvdfzswergb"
        keyApprox['v'] = "vcfbgxdertyn"
        keyApprox['b'] = "bvnghcftyun"
        keyApprox['n'] = "nńbmhjvgtuik"
        keyApprox['m'] = "mnkjloik"
        keyApprox[' '] = " "

        keyApprox['ś'] = "s"
        keyApprox['ź'] = "z"
        keyApprox['ń'] = "n"
        keyApprox['ć'] = "c"
        keyApprox['ę'] = "e"
        keyApprox['ą'] = "a"
        keyApprox['ł'] = "l"
        keyApprox['ó'] = "uo"

        probOfTypo = int(prob * 100)
        buttertext = ""
        for letter in word:
            lcletter = letter.lower()
            if not lcletter in keyApprox.keys():
                newletter = lcletter
            else:
                if random.choice(range(0, 100)) <= probOfTypo:
                    newletter = random.choice(keyApprox[lcletter])
                else:
                    newletter = lcletter
            # go back to original case
            if not lcletter == letter:
                newletter = newletter.upper()
            buttertext += newletter

        return buttertext

    @staticmethod
    def create_typos_list(words):
        global_typos = []
        for word in words:
            local_typos = []
            while len(local_typos) < 5:
                typo = RabbitmqServer.generate_typos(word)
                if typo in local_typos or typo == word:
                    pass
                else:
                    local_typos.append(typo)
            for local in local_typos:
                global_typos.append(local)
        for glob in global_typos:
            words.append(glob)
        return words
