import pika
import json
import pytest

'''
Testowanie:
1. Odpal plik textExtractor_run.py
2. RabbitMQ -> Exchanges -> format -> Publish message ->
Routing key : format.txt - > Payload: {"file": "test.txt", "words": "śląsk"} -> Publish message
3. Odpal textExtractor_test.py
'''

@pytest.fixture
def receive():
    parameters = pika.ConnectionParameters('localhost')
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    method_frame, header_frame, body = channel.basic_get(queue = 'text')
    if method_frame.NAME == 'Basic.GetEmpty':
        connection.close()
        return ''
    else:
        channel.basic_ack()
        connection.close()
        body = json.loads(body)
        return body

def test(receive):
    expected = {'file': 'test.txt', 'words': 'śląsk', 'text': 'Testing text extractor.\nLine 1\nLine 2'}
    print(receive)
    print(expected)
    assert expected == receive






