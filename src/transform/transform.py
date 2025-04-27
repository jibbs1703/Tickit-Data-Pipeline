# import json
#
# import pandas as pd
#
# from src.utils.s3 import S3Client
#
# s3_client = S3Client.credentials()
#
#
# def run_transformation(table: str) -> json:
#     return s3_client.download_file("tickit-project-bucket", f"{table}.json", "raw-files")
#
#
# tables = ["category", "date", "events", "listing", "sales", "users", "venue"]
# for t in tables:
#     data = run_transformation(t)
#     data = json.loads(data)
#     df = pd.DataFrame.from_dict(data)
#     print(df.columns)

from src.transform.transform_date import run_date_transformation

run_date_transformation()
