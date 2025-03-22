import json
from io import StringIO

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ConnectionFailure

from src.utils.logs import get_logger
from src.utils.s3 import S3Client

logger = get_logger()
s3_client = S3Client.credentials()


def connect_to_mongodb(host: str, port: int, database: str) -> Database | None:
    """
    Establish a connection to a MongoDB database.

    Returns:
    Connected database object or None if connection fails
    """
    try:
        client = MongoClient(host=host, port=port)
        client.admin.command("ping")
        logger.info("Connected to MongoDB")
        return client[database]
    except ConnectionFailure as e:
        logger.error(f"Error connecting to MongoDB: {e}")
        return None


def get_data_from_collection(db: Database, collection_name: str) -> tuple[StringIO, str] | None:
    logger.info(f"Extracting data from {collection_name}")
    collection = db[collection_name]
    documents = list(collection.find())

    if not documents:
        logger.error(f"No documents found in {collection}")
        return None

    for doc in documents:
        if "_id" in doc:
            del doc["_id"]

    json_data = json.dumps(documents)
    return StringIO(json_data), f"raw-files/{collection_name}.json"


def run_extraction(host: str, port: int, database: str, collections: list[str], bucket_name: str):
    """Run the Extraction Module Logic"""
    db = connect_to_mongodb(host, port, database)
    for collection in collections:
        body, key = get_data_from_collection(db, collection)
        s3_client.upload_file(bucket_name, key, body)
    logger.info("Data extraction completed")
