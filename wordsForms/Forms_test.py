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
"phrase": "Rycerz jest dzielny",
"filters":
{
"filetypes": ["docs", "jpeg", "mp4"],
"searchModes": [ "forms", "typos", "synonyms", "scraper"]
},
"words": []
}
3. Publish message
4. Odpal Forms_test.py
'''
@pytest.fixture
def receive():
    parameters = pika.ConnectionParameters('localhost')
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    method_frame, header_frame, body = channel.basic_get(queue = 'words.typos', auto_ack=True)
    if method_frame.NAME == 'Basic.GetEmpty':
        connection.close()
        return ''
    else:
        channel.basic_ack()
        connection.close()
        body = json.loads(body)
        return body

def test(receive):
    expected = {"path": "C:/Users/Example", "phrase":
        "Rycerz jest dzielny", "filters": {"filetypes": ["docs", "jpeg", "mp4"], "searchModes":
        ["typos", "synonyms", "scraper", "forms"]}, "words":
        ["Rycerz", "Rycerza", "Rycerzowi", "Rycerzem", "Rycerzu", "Rycerzowie", "Rycerzów",
         "Rycerzom", "Rycerzami", "Rycerzach", "Rycerze", "jest", "dzielniejszych", "dzielniejsze",
         "dzielniejszym", "dzielniejszymi", "dzielniejsi", "dzielniejszą", "dzielniejszego", "dzielniejszy",
         "dzielniejszej", "dzielniejszemu", "dzielniejsza", "dzielnych", "dzielne", "dzielnym", "dzielnymi",
         "dzielni", "dzielną", "dzielnego", "dzielny", "dzielnej", "dzielnemu", "dzielna", "najdzielniejszych",
         "najdzielniejsze", "najdzielniejszym", "najdzielniejszymi", "najdzielniejsi", "najdzielniejszą",
         "najdzielniejszego", "najdzielniejszy", "najdzielniejszej", "najdzielniejszemu", "najdzielniejsza", "dzielno"]}
    print(receive)
    print(expected)
    assert expected == receive
