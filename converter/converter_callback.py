import json
import os
import sys
import subprocess

import speech_recognition as sr

class ConverterCallback():
    log_name: str
    exchange: str
    routing_key: str
    host: str

    def __init__(self, log_name: str, exchange: str, routing_key: str, host: str):
        self.log_name = log_name
        self.exchange = exchange
        self.host = host
        self.routing_key = routing_key

    def callback(self, ch, method, properties, body):

        dir = os.path.dirname(os.getcwd())
        sys.path.insert(1, dir)

        from wordsServices_textExtractor_config import receive_config, send_connect

        message = json.loads(body)
        myfile = message["file"]
        logger = receive_config.RabbitMqServerConfigure.create_logger(self.log_name)
        logger.info(f"Received file: {myfile}")

        try:
            converter_file_path = ConverterCallback.convert(myfile)
            message["audio"]["filePathInVolume"] = converter_file_path
            message["fileState"]["fileProcessed"] = True
            message["fileState"]["fileProcessingError"] = False
            send_connect.RabbitMq.rabbit_send(message, self.host, routing_key="result", exchange="result")
            logger.info("Message was successfully forwarded with routing key: result")
        except:
            message['fileState']['fileProcessed'] = False
            message['fileState']['fileProcessingError'] = True
            # TODO: Consider adding exception to msg
            logger.warning(f'An error occurred while sending with routing key: result')
        finally:
            send_connect.RabbitMq.rabbit_send(message, self.host, self.routing_key, self.exchange)
            logger.info(f'Message was successfully forwarded with routing key: {self.routing_key}')
            logger.info(f'Published Message: {message}')

    @staticmethod
    def convert(file) -> str:
        ext = file.
        if ext == "mp3":
            subprocess.call(f"ffmpeg -i {file} -ab 160k -ac 2 -ar 44100 -vn {dst}", shell=True)

        return text_in_all_langs
