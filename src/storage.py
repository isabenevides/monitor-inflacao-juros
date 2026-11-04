import os

import boto3
from dotenv import load_dotenv

load_dotenv()

def cliente_s3():
    endpoint = os.getenv("S3_ENDPOINT_URL")
    if endpoint:
        return boto3.client(
            "s3",
            endpoint_url=endpoint,
            aws_access_key_id=os.getenv("S3_ACCESS_KEY", "local"),
            aws_secret_access_key=os.getenv("S3_SECRET_KEY", "local"),
            region_name="us-east-1",
        )
    return boto3.client("s3")  # usa ~/.aws/credentials (o aws configure)