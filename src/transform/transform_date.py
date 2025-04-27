"""Date Transformation Module"""

import json

import pandas as pd

from src.utils.s3 import S3Client


def get_date_df() -> pd.DataFrame:
    s3_client = S3Client.credentials()
    date_json = s3_client.download_file("tickit-project-bucket", "date.json", "raw-files")
    date_df = json.loads(date_json)
    return pd.DataFrame.from_dict(date_df)


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
    month_map = {
        "JAN": 1,
        "FEB": 2,
        "MAR": 3,
        "APR": 4,
        "MAY": 5,
        "JUN": 6,
        "JUL": 7,
        "AUG": 8,
        "SEP": 9,
        "OCT": 10,
        "NOV": 11,
        "DEC": 12,
    }
    df["month"] = df["month"].map(month_map)

    # Merging year, month, and day into YYYY-MM-DD format
    df["caldate"] = df[["year", "month", "day"]].astype(str).agg("-".join, axis=1)

    # Transforming caldate column into datetime type
    df["caldate"] = pd.to_datetime(df["caldate"], format="%Y-%m-%d")

    df = df[["dateid", "caldate", "qtr", "holiday"]]

    return df


def run_date_transformation() -> None:
    df = get_date_df()
    return transform_date_df(df)
