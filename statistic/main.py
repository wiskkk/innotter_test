import boto3
from fastapi import FastAPI, HTTPException

app = FastAPI()

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')


@app.get('/posts/{id}')
def post_stat(id: int):
    table = dynamodb.Table('post_stat')
    try:
        response = table.get_item(Key={
            'id': id,
        })
        return {"post stat": response['Item']}
    except KeyError:
        return HTTPException(status_code=404, detail="Item not found")


@app.get('/posts/{id}/likes')
def post_stat(id: int):
    table = dynamodb.Table('post_stat')
    try:
        response = table.get_item(Key={
            'id': id,
        })
        response = response['Item']
        return {"post likes": response['likes']}
    except KeyError:
        return HTTPException(status_code=404, detail="Item not found")


@app.get('/posts/{id}/replies')
def post_stat(id: int):
    table = dynamodb.Table('post_stat')
    try:
        response = table.get_item(Key={
            'id': id,
        })
        response = response['Item']
        return {"post replies": response['replies']}
    except KeyError:
        return HTTPException(status_code=404, detail="Item not found")


@app.get('/pages/{id}')
def page_stat(id: int):
    table = dynamodb.Table('page_stat')
    try:
        response = table.get_item(Key={
            'page_id': id,
        })
        return {"page stat": response['Item']}
    except KeyError:
        return HTTPException(status_code=404, detail="Page not found")


@app.get('/pages/{id}/followers')
def page_stat(id: int):
    table = dynamodb.Table('page_stat')
    try:
        response = table.get_item(Key={
            'page_id': id,
        })
        response = response['Item']
        return {"page followers": response['followers']}
    except KeyError:
        return HTTPException(status_code=404, detail="Not found")


@app.get('/pages/{id}/subscribers')
def page_stat(id: int):
    table = dynamodb.Table('page_stat')
    try:
        response = table.get_item(Key={
            'page_id': id,
        })
        response = response['Item']
        return {"page subscribers": response['following']}
    except KeyError:
        return HTTPException(status_code=404, detail="Not found")


@app.get('/pages/{id}/follow_requests')
def page_stat(id: int):
    table = dynamodb.Table('page_stat')
    try:
        response = table.get_item(Key={
            'page_id': id,
        })
        response = response['Item']
        return {"page follow requests": response['follow_requests']}
    except KeyError:
        return HTTPException(status_code=404, detail="Not found")
