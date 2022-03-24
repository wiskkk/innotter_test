import os

import boto3
from innotter.celery import app

client = boto3.client(
    'ses',
    region_name="us-west-2",
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
)


def verify_email_identity(email):
    ses_client = boto3.client("ses", region_name="us-west-2")
    response = ses_client.verify_email_identity(
        EmailAddress=email
    )
    print(response)


@app.task
def send_plain_email(owner, email):
    ses_client = boto3.client("ses", region_name="us-west-2")
    CHARSET = "UTF-8"
    response = ses_client.send_email(
        Destination={
            "ToAddresses": [email],
        },
        Message={
            "Body": {
                "Text": {
                    "Charset": CHARSET,
                    "Data": f"Hello, {owner} make a new post",
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": "Amazing Email Tutorial",
            },
        },
        Source=owner,
    )
