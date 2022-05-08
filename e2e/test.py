# pylint: skip-file
"""
e2e tests for whole project
"""
import pika
import json
import unittest
import time
import os

USER_PATH = os.path.expanduser('~')
PATH = os.getcwd()
HOME_PATH = PATH.replace(USER_PATH, '~') + '/test-dir'


class TestSum(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = connection.channel()

    def wait_for_message(self, sleep, count):
        """
        Method implementing blocking message consuming
        """
        for _i in range(count):
            res = self.channel.basic_get(queue='result')
            if res == (None, None, None):
                time.sleep(sleep)
            else:
                (method, _, body) = res
                self.channel.basic_ack(method.delivery_tag)
                body_string = body.decode("utf-8")
                return json.loads(body_string)

        raise TimeoutError("Did not receive any message in given time")

    def test_should_find_phrase_in_text_file(self):
        # given
        mock_request = {
            "phrase": "text",
            "path": HOME_PATH,
            "filters": {
                "fileTypes": [".txt"],
                "filterModes":[]
            },
            "words":["text"]
        }
        
        # when
        self.channel.basic_publish(exchange='words', routing_key='words.scraper', body=json.dumps(mock_request))
        res = self.wait_for_message(0.5, 5)

        # then
        self.assertEqual(res['text'], 'this is some random text with random words')
        self.assertEqual(res['found'], True)


if __name__ == '__main__':
    unittest.main()




