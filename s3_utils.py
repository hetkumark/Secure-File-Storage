import boto3
from config import AWS_ACCESS_KEY, AWS_SECRET_KEY, S3_BUCKET_NAME

def upload_to_s3(bucket_name, file_name, file_data):
    """Uploads a file to the specified S3 bucket."""
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )
    s3.put_object(Bucket=bucket_name, Key=file_name, Body=file_data)
    print(f"File {file_name} uploaded successfully to {bucket_name}")

def download_from_s3(bucket_name, file_name):
    """Downloads a file from the specified S3 bucket."""
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )
    obj = s3.get_object(Bucket=bucket_name, Key=file_name)
    return obj["Body"].read()
