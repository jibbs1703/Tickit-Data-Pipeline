from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.transform.transform import get_df_from_s3


@patch("src.transform.transform.S3Client")
def test_get_df_from_s3_success(mock_s3_client_class):
    # Arrange
    mock_s3_client = MagicMock()
    mock_s3_client_class.credentials.return_value = mock_s3_client
    # Simulate a JSON string representing a list of dicts
    test_json = '[{"col1": 1, "col2": "a"}, {"col1": 2, "col2": "b"}]'
    mock_s3_client.download_file.return_value = test_json

    # Act
    df = get_df_from_s3("bucket", "file.json", "folder")

    # Assert
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["col1", "col2"]
    assert df.shape == (2, 2)
    assert df.iloc[0]["col1"] == 1
    assert df.iloc[1]["col2"] == "b"


@patch("src.transform.transform.S3Client")
def test_get_df_from_s3_no_file(mock_s3_client_class):
    # Arrange
    mock_s3_client = MagicMock()
    mock_s3_client_class.credentials.return_value = mock_s3_client
    mock_s3_client.download_file.return_value = None

    # Act & Assert
    with pytest.raises(ValueError, match="No json file accessed."):
        get_df_from_s3("bucket", "file.json", "folder")
