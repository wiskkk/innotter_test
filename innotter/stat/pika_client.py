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
        print('Соединение Pika инициализировано')

    async def consume(self, loop):
        """Настроить прослушиватель сообщений с текущим запущенным циклом"""
        print(1)
        connection = await connect_robust(
            'amqps://rtmsnwel:5SH5XtlcRwDYNCUYp9O7q3KIAiPqJKbJ@rat.rmq2.cloudamqp.com/rtmsnwel',
            loop=loop)
        print(2)
        channel = await connection.channel()
        print(3)
        queue = await channel.declare_queue('CONSUME_QUEUE')
        print(4)
        await queue.consume(self.process_incoming_message, no_ack=True)  # no_ack=False
        print(5)
        print('Установленный асинхронный слушатель pika')
        return connection

    def process_incoming_message(self, message):
        """Обработка входящего сообщения от RabbitMQ"""
        print(6)
        # message.ack()
        print(7)
        body = message.body
        print(8)
        print('Полученное сообщение')
        print(9)
        if body:
            print(10)
            self.process_callable(json.loads(body))


    # def send_message(self, message: dict):
    #     """Метод публикации сообщения в RabbitMQ"""
    #     print(11)
    #     self.channel.basic_publish(
    #         exchange='',
    #         routing_key=self.publish_queue_name,
    #         properties=pika.BasicProperties(
    #             reply_to=self.callback_queue,
    #         ),
    #         body=json.dumps(message)
    #     )
