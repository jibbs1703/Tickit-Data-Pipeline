import json

import pandas as pd

from utils.s3 import S3Client


def get_df_from_s3(bucket_name: str, file_name: str, folder: str) -> pd.DataFrame:
    s3_client = S3Client.credentials()
    json_file = s3_client.download_file(
        bucket_name=bucket_name, object_name=file_name, folder=folder
    )
    if json_file is None:
        raise ValueError("No json file accessed.")
    df = json.loads(json_file)
    return pd.DataFrame.from_dict(df)


def transform_date_df(df: pd.DataFrame) -> pd.DataFrame:
    with open("src/utils/transform.json") as file:
        transform_json = json.load(file)
    month_map = transform_json["month_map"]

    df["month"] = df["month"].map(month_map)

    # Merging year, month, and day into YYYY-MM-DD format
    df["caldate"] = df[["year", "month", "day"]].astype(str).agg("-".join, axis=1)

    # Transforming caldate column into datetime type
    df["caldate"] = pd.to_datetime(df["caldate"], format="%Y-%m-%d")

    df = df[["dateid", "caldate", "qtr", "holiday"]]

    return df


df = get_df_from_s3(bucket_name="tickit-project-bucket", file_name="date.json", folder="raw-files")
df = transform_date_df(df)
print(df.head())
