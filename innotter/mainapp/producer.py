import json
import os

import pika

conn_params = pika.URLParameters(os.environ.get("URL_PARAMS"))
connection = pika.BlockingConnection(conn_params)
channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='',
                          routing_key='statistics',
                          body=json.dumps(body), properties=properties)
