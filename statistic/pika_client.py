import json

import pika
from aio_pika import connect_robust


class PikaClient:

    def __init__(self, process_callable):
        self.publish_queue_name = 'PUBLISH_QUEUE'
        self.connection = pika.BlockingConnection(
            pika.URLParameters('amqps://rtmsnwel:5SH5XtlcRwDYNCUYp9O7q3KIAiPqJKbJ@rat.rmq2.cloudamqp.com/rtmsnwel')
        )
        self.channel = self.connection.channel()
        self.publish_queue = self.channel.queue_declare(queue=self.publish_queue_name)
        self.callback_queue = self.publish_queue.method.queue
        self.response = None
        self.process_callable = process_callable
        print('Pika connection initialized')

    async def consume(self, loop):
        """Setup message listener with the current running loop"""
        connection = await connect_robust(
            'amqps://rtmsnwel:5SH5XtlcRwDYNCUYp9O7q3KIAiPqJKbJ@rat.rmq2.cloudamqp.com/rtmsnwel',
            loop=loop)
        channel = await connection.channel()
        queue = await channel.declare_queue('CONSUME_QUEUE')
        await queue.consume(self.process_incoming_message, no_ack=False)
        print('Established pika async listener')
        return connection

    async def process_incoming_message(self, message):
        """Processing incoming message from RabbitMQ"""
        message.ack()
        body = message.body
        print('Received message')
        if body:
            self.process_callable(json.loads(body))

    def send_message(self, message: dict):
        """Method to publish message to RabbitMQ"""
        self.channel.basic_publish(
            exchange='',
            routing_key=self.publish_queue_name,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
            ),
            body=json.dumps(message)
        )
