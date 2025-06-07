"""Date Transformation Module"""

import json

import pandas as pd

from src.utils.s3 import S3Client


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
    """
    Transforms the Date DataFrame by performing the following operations:

    1. Maps the contents of the 'month' column from three-letter abbreviations
       (e.g., 'JAN', 'FEB', etc.) to their corresponding integer values (1-12).
    2. Combines the 'year', 'month', and 'day' columns into a new column 'caldate'
       in the format YYYY-MM-DD.
    3. Converts the 'caldate' column into a datetime type for easier date manipulation.

    Args:
    df (pd.DataFrame): The input DataFrame containing 'year', 'month', and 'day' columns.

    Returns:
    pd.DataFrame: A transformed DataFrame with an updated 'month' column,
                  a new 'caldate' column, and 'caldate' converted to datetime.
    """
    # Mapping month abbreviations to integers
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
