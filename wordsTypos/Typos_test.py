import pika
import json
import pytest

'''
Testowanie:
    !!!
Typos_receive zwraca losowe wygenerowane typosy, za każdym razem inne.
Funkcja testowa porównuje jedynie czy wylosowano po 5 typosów dla każdego słowa.
    !!!
1. Odpal plik wordsTypos_run.py

2. RabbitMQ -> Exchanges -> words -> Publish message ->
Routing key : words.typos - > Payload: 
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
4. Odpal Typos_test.py
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
    expected = {'path': 'C:/Users/Example', 'phrase': 'alamakota', 'queueKey': 'words.forms', 'filters': {'filetypes': ['docs', 'jpeg', 'mp4'], 'searchModes': ['synonyms', 'typos', 'forms', 'scraper']}, 'words': ['długi', 'Rycerz', 'dłudi', 'dłuci', 'dłhgi', 'dlugi', 'dłógi', 'Gycerz', 'Rycerd', 'Vycerz', 'Ryderz', 'Rycecz']}
    print(receive)
    print(expected)
    assert len(expected['words']) == len(receive['words'])