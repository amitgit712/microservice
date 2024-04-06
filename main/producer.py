import pika
import json

params = pika.URLParameters('replace with your credentials')

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(
        exchange='', routing_key='admin',
        body=json.dumps(body), properties=properties
    )
