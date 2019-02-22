import logging
import os

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

S3_REGION = os.environ['S3_REGION']
S3_ENDPOINT = os.environ['S3_ENDPOINT']

client = boto3.client('s3', region_name=S3_REGION, endpoint_url=S3_ENDPOINT)


class S3FileUploadException(Exception): pass


class S3FileAlreadyExistsException(Exception): pass


def put_object_into_s3(bucket_name, bucket_key, body):
    response = client.put_object(Bucket=bucket_name, Key=bucket_key, Body=body)
    status_code = response['ResponseMetadata']['HTTPStatusCode']

    logger.debug(f"S3 put object status: {status_code} for s3://{bucket_name}/{bucket_key}")

    return response


def get_object_from_s3(bucket_name, bucket_key):
    response = client.get_object(Bucket=bucket_name, Key=bucket_key)
    status_code = response['ResponseMetadata']['HTTPStatusCode']

    logger.debug(f"S3 get object status: {status_code} for s3://{bucket_name}/{bucket_key}")

    return response


def check_if_file_exists(bucket_name, bucket_key):
    """Return the key's size if it exist, else None"""

    response = client.list_objects_v2(
        Bucket=bucket_name,
        Prefix=bucket_key,
    )
    for obj in response.get('Contents', []):
        if obj['Key'] == bucket_key:
            return obj['Size']

