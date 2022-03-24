import json
import sys
import traceback

import pika

# from .models import Page
import mainapp.models

conn_params = pika.URLParameters('amqps://rtmsnwel:5SH5XtlcRwDYNCUYp9O7q3KIAiPqJKbJ@rat.rmq2.cloudamqp.com/rtmsnwel')
connection = pika.BlockingConnection(conn_params)
# connection = pika.BlockingConnection(pika.URLParameters("amqp://guest:guest@rabbitmq/"))
channel = connection.channel()

channel.queue_declare(queue='statistics')


def callback(ch, method, properties, body):
    print('received in statistics')
    print(body)
    data = json.loads(body)
    print(data)
    print(type(data))

    if properties.content_type == 'page_created':
        page = mainapp.models.Post(name=data['name'], posts=data['posts'], followers=data['followers'],
                                   following=['following'], follow_requests=data['follow_requests'])
        print()
        page.save()
        print('page created')
    elif properties.content_type == 'post_created':
        post = mainapp.models.Post(name=data['name'], content=data['content'], like=data['like'], replies=['replies'])
        print(post)
        post.save()
        print('post created')
    elif properties.content_type == 'post_updated':
        post = mainapp.models.Post(name=data['name'], content=data['content'], like=data['like'], replies=['replies'])
        post.save()
        print(post)
        print('post created')


channel.basic_consume(queue='statistics', on_message_callback=callback, auto_ack=True)

try:
    channel.start_consuming()
    print('started consuming by statistic')

except KeyboardInterrupt:
    channel.stop_consuming()
    print('stopped by keyboard')
except Exception:
    channel.stop_consuming()
    traceback.print_exc(file=sys.stdout)

# channel.start_consuming()

channel.close()
