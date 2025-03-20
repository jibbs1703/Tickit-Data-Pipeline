from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ConnectionFailure

from src.utils.logger import get_logger

logger = get_logger()


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


if __name__ == "__main__":
    MONGO_HOST: str = "localhost"
    MONGO_PORT: int = 27017
    MONGO_DB: str = "tickit"
    db = connect_to_mongodb(host=MONGO_HOST, port=MONGO_PORT, database=MONGO_DB)
