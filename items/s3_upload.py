import os

import boto3
import logging

AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY']
AWS_SECRET_KEY = os.environ['AWS_SECRET_KEY']
AWS_REGION = 'us-east-1'
BUCKET_NAME = 'namespace'
FILE_NAME_S3 = 'resume.docx'


def upload_file(file):
    try:
        client = boto3.client(service_name='s3', region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY,
                              aws_secret_access_key=AWS_SECRET_KEY)
        result = client.put_object(Body=file, Bucket=BUCKET_NAME, Key=FILE_NAME_S3,
                                   ContentType='application/octet-stream')
        return result
    except Exception as e:
        logging.error("failed uploading file to S3: ", repr(e))
        raise e