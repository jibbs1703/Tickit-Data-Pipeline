"""Module to transform tickit data into a pandas DataFrame."""

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
    """Perform transformations on the date DataFrame.
    This function performs the following transformations:
    1. Maps month numbers to month names.
    2. Merges year, month, and day into a single date column in YYYY-MM-DD format.
    3. Converts the date column to datetime type.

    Args:
        df (pd.DataFrame): The date DataFrame to transform.

    Returns:
        df (pd.DataFrame): The transformed date DataFrame with columns:
            - dateid: Unique identifier for the date.
            - caldate: Date in YYYY-MM-DD format.
            - qtr: Quarter of the year.
            - holiday: Indicates if the date is a holiday.
    """
    with open("src/utils/transform.json") as file:
        transform_json = json.load(file)
    month_map = transform_json["month_map"]
    df["month"] = df["month"].map(month_map)
    # Merging year, month, and day into YYYY-MM-DD format
    df["caldate"] = df[["year", "month", "day"]].astype(str).agg("-".join, axis=1)
    # Transforming caldate column into datetime type
    df["caldate"] = pd.to_datetime(df["caldate"], format="%Y-%m-%d")
    # Selecting relevant columns
    df = df[["dateid", "caldate", "qtr", "holiday"]]

    return df


def transform_users_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Perform transformations the users DataFrame.

    This function performs the following transformations:
    1. Maps state abbreviations to full state names.
    2. Fills missing state values with 'Non-US State'.
    3. Adds country code to phone numbers.

    """
    # Load the transformation mappings from the JSON file
    with open("src/utils/transform.json") as file:
        transform_json = json.load(file)
    abbreviate = transform_json["abbreviationToState"]
    # Map state abbreviations to full state names
    df["state"] = df["state"].map(abbreviate)
    # Fill missing state values with 'Non-US State'
    df["state"].fillna("Non-US State", inplace=True)
    # Add country code to phone numbers
    df["phone"] = df["phone"].apply(lambda x: f"+1 {x}" if pd.notnull(x) else x)
    return df
