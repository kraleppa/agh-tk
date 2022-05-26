import json
import os
import sys

import speech_recognition as sr

class AudioExtractorCallback():
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
            text_from_audio = AudioExtractorCallback.extract(myfile)
            message["text"] = text_from_audio
            message["fileState"]["fileProcessed"] = True
            message["fileState"]["fileProcessingError"] = False
            send_connect.RabbitMq.rabbit_send(message, self.host, routing_key="result", exchange="result")
            logger.info("Message was successfully forwarded with routingkey: result")
        except:
            message['fileState']['fileProcessed'] = False
            message['fileState']['fileProcessingError'] = True
            # TODO: Add exception to msg
            logger.warning(f'An error occurred while sending with routing key: result')
        finally:
            send_connect.RabbitMq.rabbit_send(message, self.host, self.routing_key, self.exchange)
            logger.info(f'Message was successfully forwarded with routing key: {self.routing_key}')
            logger.info(f'Published Message: {message}')

    @staticmethod
    def extract(file) -> str:
        langs = ["en-US", "pl"]
        r = sr.Recognizer()
        file = os.path.join(file)

        text_in_all_langs = ""

        try:
            with sr.AudioFile(file) as source:
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.record(source)
                for lang in langs:
                    try:
                        text_in_all_langs = f"{text_in_all_langs}\n{r.recognize_google(audio, language=lang)}"
                    except sr.UnknownValueError:
                        raise Exception(f"{file}: Google Speech Recognition could not understand audio")
                    except sr.RequestError:
                        raise Exception(f"{file}: Could not request results from Google Speech Recognition service")
        except Exception:
            raise Exception(f"{file}: Error while converting file to audio")

        return text_in_all_langs
