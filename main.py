"""Main Entry Point to Run Data Pipeline"""

import argparse

from src.extract.extract import run_extract

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Connect to MongoDB.")

    parser.add_argument("--host", type=str, default="localhost", help="MongoDB host address")
    parser.add_argument("--port", type=int, default=27017, help="MongoDB port number")
    parser.add_argument("--database", type=str, default="tickit", help="MongoDB database name")
    parser.add_argument(
        "--bucket_name",
        type=str,
        default="tickit-project-bucket",
        help="Target S3 bucket name",
    )
    parser.add_argument(
        "--collections",
        type=str,
        nargs="+",
        default=["users"],
        help="MongoDB collection names",
    )
    args = parser.parse_args()

    run_extract(
        host=args.host,
        port=args.port,
        database=args.database,
        collections=args.collections,
        bucket_name=args.bucket_name,
    )
