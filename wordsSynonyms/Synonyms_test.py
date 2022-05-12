import pika
import json
import pytest

'''
Testowanie:
1. Odpal plik wordsSynonyms_run.py

2. RabbitMQ -> Exchanges -> words -> Publish message ->
Routing key : words.synonyms - > Payload: 
{
"path": "C:/Users/Example",
"phrase": "Rycerz jest dzielny",
"filters":
{
"filetypes": ["docs", "jpeg", "mp4"],
"searchModes": [ "synonyms", "typos", "forms", "scraper"]
},
"words": []
}
3. Publish message
4. Odpal Synonyms_test.py
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
        "Rycerz jest dzielny", "filters":
        {"filetypes": ["docs", "jpeg", "mp4"], "searchModes":
            ["typos", "forms", "scraper", "synonyms"]}, "words":
        ["Rycerz", "jest", "dzielny", "rycerz", "feudał", "szlachcic", "wojownik", "żołnierz",
         "mężny", "nieugięty", "nieulękły", "nieustraszony", "niezmordowany", "niezniechęcony",
         "niezrażony", "odważny", "odporny", "śmiały", "wytrwały", "wytrzymały"]}
    print(receive)
    print(expected)
    assert expected == receive

