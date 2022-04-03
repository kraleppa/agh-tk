import pika
from send import send

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()

queue = channel.queue_declare('format.txt', durable = True)
queue_name = queue.method.queue

def callback(ch, method, properties, body):
    send(body)

channel.basic_consume(on_message_callback=callback, queue=queue_name, auto_ack=True)

# print('Waiting for message.')

channel.start_consuming()
