import json
import os
import sys
import traceback

import boto3
import pika

conn_params = pika.URLParameters(os.environ.get("URL_PARAMS"))
connection = pika.BlockingConnection(conn_params)
channel = connection.channel()
print('consumer start')
channel.queue_declare(queue='statistics')


def callback(ch, methods, properties, body):
    print('received in statistics')
    data = json.loads(body)

    if properties.content_type == 'page_created':
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.Table('page_stat')

        response = table.put_item(
            Item=json.loads(body.decode('utf-8'))
        )
        print('page_created')
        print(response)
    elif properties.content_type == 'page_updated':
        body = json.loads(body.decode('utf-8'))
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.Table('page_stat')

        id = data['id']
        response = table.update_item(
            Key={
                'page_id': id,
            },
            UpdateExpression="set page_owner=:o, page_name=:n, followers=:fs, following=:fg, follow_requests=:fr",
            ExpressionAttributeValues={
                ':o': body['owner'],
                ':n': body['name'],
                ':fs': body['followers'],
                ':fg': body['following'],
                ':fr': body['follow_requests'],
            },
            ReturnValues="UPDATED_NEW"
        )
        print('page updated')
        print(response)
    elif properties.content_type == 'post_created':
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.Table('post_stat')

        response = table.put_item(
            Item=json.loads(body.decode('utf-8'))
        )
        print('post created')
        print(response)

    elif properties.content_type == 'post_updated':
        body = json.loads(body.decode('utf-8'))
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.Table('post_stat')

        id = data['id']
        response = table.update_item(
            Key={
                'id': id,
            },
            UpdateExpression="set page=:p, content=:c, replies=:r, likes=:l",
            ExpressionAttributeValues={
                ':p': body['page'],
                ':c': body['content'],
                ':r': body['replies'],
                ':l': body['like'],
            },
            ReturnValues="UPDATED_NEW"
        )
        print('post updated')
        print(response)


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

channel.close()
