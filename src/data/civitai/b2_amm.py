import boto3  # REQUIRED! - Details here: https://pypi.org/project/boto3/
from botocore.exceptions import ClientError
from botocore.config import Config
import os


def get_b2_resource(endpoint: str, key_id: str, application_key: str):
    b2 = boto3.resource(service_name='s3',
                        endpoint_url=endpoint,  # Backblaze endpoint
                        aws_access_key_id=key_id,  # Backblaze keyID
                        aws_secret_access_key=application_key,  # Backblaze applicationKey
                        config=Config(
                            signature_version='s3v4',
                        ))
    return b2


endpoint = "https://s3.us-west-001.backblazeb2.com"
key_id = "0010405dbf98c260000000001"
application_key = "K0013htjR12edTq+zAR+XXUuPSVsg6M"

b2_rw = get_b2_resource(endpoint, key_id, application_key)

os.system(f"b2 authorize_account {key_id} {application_key}")

def upload_file(bucket: str, directory: str, file: str, b2, b2path=None) -> None:
    file_path = directory + '/' + file
    remote_path = b2path
    if remote_path is None:
        remote_path = file
    try:
        response = b2.Bucket(bucket).upload_file(file_path, remote_path)
    except ClientError as ce:
        print('error', ce)


def upload_amm(fullpath: str, filename: str) -> None:
    # b2_rw.Bucket("amm-001").upload_file(fullpath, filename)
    os.system(f'b2 upload-file amm-001 "{fullpath}" {filename}')

