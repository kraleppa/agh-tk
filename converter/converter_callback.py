import json
import os
import sys
import subprocess

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
            converter_file_path = ConverterCallback.convert(myfile, logger)
            message["audio"] = {}
            message["audio"]["filePathInVolume"] = converter_file_path
            message["fileState"]["fileProcessed"] = True
            message["fileState"]["fileProcessingError"] = False
            send_connect.RabbitMq.rabbit_send(message, self.host, routing_key="result", exchange="result")
            logger.info("Message was successfully forwarded with routing key: result")
        except Exception as e:
            message['fileState']['fileProcessed'] = False
            message['fileState']['fileProcessingError'] = True
            logger.warning(f'An error occurred while converting or sending with routing key: result, err: {e}')
        finally:
            send_connect.RabbitMq.rabbit_send(message, self.host, self.routing_key, self.exchange)
            logger.info(f'Message was successfully forwarded with routing key: {self.routing_key}')
            logger.info(f'Published Message: {message}')

    @staticmethod
    def convert(file, logger) -> str:
        filename = os.path.basename(file)
        name, ext = os.path.splitext(filename)

        output_dir = f"/host/extracted/{ext}-converted"
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        dst = os.path.abspath(os.path.join(output_dir, f"{name}.wav"))

        if os.path.exists(dst):
            logger.info(f"{dst} file already exists, returning it")
            return dst

        logger.info(f"Dst file = {dst}")

        if ext == ".mp3":
            subprocess.call(f"ffmpeg -i {file} {dst}", shell=True)
        elif ext == ".mp4":
            subprocess.call(f"ffmpeg -i {file} -ab 160k -ac 2 -ar 44100 -vn {dst}", shell=True)
        else:
            raise Exception(f"Unsupported conversion extension {ext}")

        return dst
