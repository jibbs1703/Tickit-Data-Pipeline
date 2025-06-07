import os
from io import StringIO

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

from utils.logs import get_logger

logger = get_logger()


class S3Client:
    @classmethod
    def credentials(cls) -> "S3Client":
        """
        Retrieves AWS credentials from a hidden environment file.

        This class method accesses the user's AWS secret and access
        keys stored in an environment file. If a region is specified,
        the methods within the S3Client class will execute in that region.
        Otherwise, AWS will assign a default region.

        :return: An instance of the S3Client class initialized with
        the user's credentials and specified region
        """
        load_dotenv()
        secret = os.getenv("ACCESS_SECRET")
        access = os.getenv("ACCESS_KEY")
        region = os.getenv("REGION")

        return cls(secret, access, region)

    def __init__(self, secret, access, region) -> None:
        """
        Initializes the S3Client class with user credentials and creates
        the AWS S3 client.

        This constructor method initializes the S3Client class using the
        provided secret and access keys. It creates an AWS S3 client using
        the boto3 library. If no region is specified, AWS assigns the default
        region identified via aws-cli. The created client is available for
        subsequent methods within the class.

        :param secret: User's AWS secret key loaded from the environment file
        :param access: User's AWS access key loaded from the environment file
        :param region: User's AWS region loaded from the environment file

        Returns: None
        """
        if region is None:
            self.client = boto3.client("s3", aws_access_key_id=access, aws_secret_access_key=secret)
        else:
            self.location = {"LocationConstraint": region}
            self.client = boto3.client(
                "s3",
                aws_access_key_id=access,
                aws_secret_access_key=secret,
                region_name=region,
            )

    def upload_file(self, bucket_name: str, key: str, body: StringIO) -> None:
        """
        Uploads a file to an S3 bucket.
        Parameters:
        - bucket_name (str): The name of the target S3 bucket.
        - key (str): The key (path) under which the file will be stored in the bucket.
        - body (StringIO): The file content to be uploaded.

        Returns: None
        """
        try:
            self.client.put_object(Bucket=bucket_name, Key=key, Body=body.getvalue())
            logger.info(f"File uploaded successfully to {bucket_name} as {key}")
        except ClientError as e:
            logger.error(f"Error uploading file to S3: {str(e)}")

        except ConnectionError as e:
            logger.error(f"Error uploading file to S3: {str(e)}")

    def download_file(self, bucket_name: str, object_name: str, folder: str = "") -> None:
        """
        Downloads a file from an S3 bucket in the user's AWS account.

        :param bucket_name: Name of the bucket to download the file from
        :param object_name: Name of the file to download from the S3 bucket
        :param folder: The folder path within the S3 bucket.
          Default is an empty string.

        Returns: None
        """
        try:
            response = self.client.get_object(Bucket=bucket_name, Key=f"{folder}/{object_name}")
            logger.info(f"File '{object_name}' read successfully from bucket")
            return response["Body"].read().decode("utf-8")

        except ClientError as e:
            logger.error(f"Client Error downloading file: {e}")

        except Exception as e:
            logger.exception(f"Unexpected error downloading file: {e}")
