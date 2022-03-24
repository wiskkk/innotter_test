import json

import pika

conn_params = pika.URLParameters('amqps://rtmsnwel:5SH5XtlcRwDYNCUYp9O7q3KIAiPqJKbJ@rat.rmq2.cloudamqp.com/rtmsnwel')
connection = pika.BlockingConnection(conn_params)
channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='',
                          routing_key='statistics',
                          body=json.dumps(body), properties=properties)
