"""Tests for the extract module."""

from unittest.mock import MagicMock

import pytest
from pymongo.errors import ConnectionFailure

from src.extract.extract import connect_to_mongodb


@pytest.mark.unit
def test_successful_connection(mock_connection):
    """Test the successful connection to MongoDB."""
    mock_client = MagicMock()
    mock_connection.return_value = mock_client

    db_name = "test_db"
    result = connect_to_mongodb("localhost", 27017, db_name)

    # Check if MongoClient was called with correct arguments
    mock_connection.assert_called_once_with(host="localhost", port=27017)

    # Check if the ping command was executed
    mock_client.admin.command.assert_called_once_with("ping")

    # Assert the returned database object is correct
    assert result == mock_client[db_name]


@pytest.mark.unit
def test_failed_connection(mock_connection):
    """Simulate a ConnectionFailure exception"""
    mock_client = MagicMock()
    mock_connection.return_value = mock_client
    mock_connection.side_effect = ConnectionFailure("Connection failed")

    result = connect_to_mongodb("localhost", 27017, "test_db")

    # Ensure result is None when connection fails
    assert result is None
