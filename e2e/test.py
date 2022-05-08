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
VOLUME_PATH = HOME_PATH.replace('~', '/host')


class E2ETests(unittest.TestCase):
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
        self.assertEqual(res['file'], f"{VOLUME_PATH}/test.txt")
        self.assertEqual(res['text'], 'this is some random text with random words')
        self.assertEqual(res['found'], True)

    def test_should_find_phrase_in_images(self):
        # given
        mock_request = {
            "phrase": "some",
            "path": HOME_PATH,
            "filters": {
                "fileTypes": [".png"],
                "filterModes":[]
            },
            "words":["some"]
        }

        # when
        self.channel.basic_publish(exchange='words', routing_key='words.scraper', body=json.dumps(mock_request))
        res1 = self.wait_for_message(0.5, 5)
        res2 = self.wait_for_message(0.5, 5)

        # then
        self.assertSetEqual({res1['file'], res2['file']}, {f"{VOLUME_PATH}/test2.png", f"{VOLUME_PATH}/some-photos/test1.png"})
        self.assertSetEqual({res1['found'], res2['found']}, {True, False})

    def test_should_find_phrase_in_docx(self):
        # given
        mock_request = {
            "phrase": "some",
            "path": HOME_PATH,
            "filters": {
                "fileTypes": [".docx"],
                "filterModes":[]
            },
            "words":["some"]
        }

        # when
        self.channel.basic_publish(exchange='words', routing_key='words.scraper', body=json.dumps(mock_request))
        res = self.wait_for_message(0.5, 5)

        # then
        self.assertEqual(res['file'], f"{VOLUME_PATH}/test.docx")
        self.assertEqual(res['found'], True)

    def test_should_find_phrase_in_pptx_title(self):
        # given
        mock_request = {
            "phrase": "cool",
            "path": HOME_PATH,
            "filters": {
                "fileTypes": [".pptx"],
                "filterModes":[]
            },
            "words":["cool"]
        }

        # when
        self.channel.basic_publish(exchange='words', routing_key='words.scraper', body=json.dumps(mock_request))
        res = self.wait_for_message(0.5, 5)

        # then
        self.assertEqual(res['file'], f"{VOLUME_PATH}/test.pptx")
        self.assertEqual(res['found'], True)

    def test_should_find_phrase_in_pptx_body(self):
        # given
        mock_request = {
            "phrase": "marynarzem",
            "path": HOME_PATH,
            "filters": {
                "fileTypes": [".pptx"],
                "filterModes":[]
            },
            "words":["marynarzem"]
        }

        # when
        self.channel.basic_publish(exchange='words', routing_key='words.scraper', body=json.dumps(mock_request))
        res = self.wait_for_message(0.5, 5)

        # then
        self.assertEqual(res['file'], f"{VOLUME_PATH}/test.pptx")
        self.assertEqual(res['found'], True)



if __name__ == '__main__':
    unittest.main()




