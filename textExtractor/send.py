import pika
import json
import os

def send(path):
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()

    channel.exchange_declare(
        exchange = 'text',
        exchange_type = 'direct',
        passive = True,
        durable = True
    )
    
    path = os.path.join(path)

    with open(path,'r') as f:
        print(f'Received path: {path}')
        msg = f.read()


    channel.basic_publish(
        exchange='text',
        routing_key='text',
        body = json.dumps(msg)
    )

    connection.close()
