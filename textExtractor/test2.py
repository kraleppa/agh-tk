import pika
import json
import os

'''
Testowanie:
1. Odpal plik receive.py

2. RabbitMQ -> Exchanges -> format -> Publish message ->
Routing key : format.txt - > Payload: {"file": "test.txt", "words": "word"} -> Publish message
3.
4. Odpal test2.py
'''

def exp(file):
    myfile = file['file']
    extracted = extract(myfile)
    file["text"] = extracted
    return file

def extract(file):
    file = os.path.join(file)
    with open(file, 'r') as f:
        msg = f.read()
    return msg

def test():
    file = {"file": "test.txt", "words": "word"}
    expected = exp(file)
    parameters = pika.ConnectionParameters('localhost')
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='text', passive=True, durable=True)
    method_frame, header_frame, body = channel.basic_get(queue = 'text')
    if method_frame.NAME == 'Basic.GetEmpty':
        connection.close()
        return ''
    else:
        channel.basic_ack()
        connection.close()
        body = json.loads(body)
    print('\n',body)
    print(expected)
    assert body == expected
    print(type(body))
    print(type(expected))
    assert type(body) == type(expected)

if __name__ == "__main__":
    test()





