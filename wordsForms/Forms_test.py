import pika
import json
import pytest

'''
Testowanie:
1. Odpal plik wordForms_run.py

2. RabbitMQ -> Exchanges -> words -> Publish message ->
Routing key : words.forms - > Payload: 
{
"path": "C:/Users/Example",
"phrase": "alamakota", 
"queueKey": "words.forms", 
"filters": 
{
"filetypes": ["docs", "jpeg", "mp4"], 
"searchModes": ["synonyms", "typos", "forms", "scraper"]
}, 
"words": ["długi", "Rycerz"]
}
3. Publish message
4. Odpal Forms_test.py
'''
@pytest.fixture
def receive():
    parameters = pika.ConnectionParameters('localhost')
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='words.scraper', passive=True, durable=True)
    method_frame, header_frame, body = channel.basic_get(queue = 'words.scraper')
    if method_frame.NAME == 'Basic.GetEmpty':
        connection.close()
        return ''
    else:
        channel.basic_ack()
        connection.close()
        body = json.loads(body)
        return body

def test(receive):
    expected = {'path': 'C:/Users/Example', 'phrase': 'alamakota', 'queueKey': 'words.forms',
                'filters': {'filetypes': ['docs', 'jpeg', 'mp4'], 'searchModes': ['synonyms', 'typos', 'forms', 'scraper']},
                'words': ['długich', 'długie', 'długim', 'długimi', 'dłudzy', 'długą', 'długiego', 'długi', 'długiej',
                          'długiemu', 'długa', 'najdłuższych', 'najdłuższe', 'najdłuższym', 'najdłuższymi', 'najdłużsi',
                          'najdłuższą', 'najdłuższego', 'najdłuższy', 'najdłuższej', 'najdłuższemu', 'najdłuższa', 'dłuższych',
                          'dłuższe', 'dłuższym', 'dłuższymi', 'dłużsi', 'dłuższą', 'dłuższego', 'dłuższy', 'dłuższej', 'dłuższemu',
                          'dłuższa', 'długo', 'Rycerz', 'Rycerza',
                                                                                                                                                                                                                     'Rycerzowi', 'Rycerzem', 'Rycerzu', 'Rycerzowie', 'Rycerzów', 'Rycerzom', 'Rycerzami', 'Rycerzach', 'Rycerze']}
    print(receive)
    print(expected)
    assert expected == receive
