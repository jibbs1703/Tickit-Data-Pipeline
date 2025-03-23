from src.utils.logs import get_logger
from src.utils.s3 import S3Client

s3_client = S3Client.credentials()
logger = get_logger()


def run_transformation():
    return s3_client.download_file("tickit-project-bucket", "events.json", "raw-files")
