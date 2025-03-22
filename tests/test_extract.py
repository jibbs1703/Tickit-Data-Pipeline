"""Tests for the extract module."""

import json
from io import StringIO
from unittest.mock import MagicMock

import pytest
from pymongo.errors import ConnectionFailure

from src.extract.extract import connect_to_mongodb, get_data_from_collection


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


def test_get_data_from_collection_success(mock_db, mock_logger):
    mock_db_instance, mock_collection = mock_db
    documents = [{"_id": 1, "name": "test1"}, {"_id": 2, "name": "test2"}]
    mock_collection.find.return_value = documents

    result = get_data_from_collection(mock_db_instance, "test_collection")

    mock_db_instance.__getitem__.assert_called_once_with("test_collection")
    mock_collection.find.assert_called_once()
    assert result is not None
    assert isinstance(result[0], StringIO)
    assert result[1] == "raw-files/test_collection.json"
    expected_data = [{"name": "test1"}, {"name": "test2"}]
    assert json.loads(result[0].getvalue()) == expected_data
    mock_logger.info.assert_called_with("Extracting data from test_collection")


def test_get_data_from_collection_no_documents(mock_db, mock_logger):
    mock_db_instance, mock_collection = mock_db
    mock_collection.find.return_value = []

    result = get_data_from_collection(mock_db_instance, "test_collection")

    mock_db_instance.__getitem__.assert_called_once_with("test_collection")
    mock_collection.find.assert_called_once()
    assert result is None
    mock_logger.error.assert_called_with(f"No documents found in {mock_collection}")


def test_get_data_from_collection_no_id_field(mock_db, mock_logger):
    mock_db_instance, mock_collection = mock_db
    documents = [{"name": "test1"}, {"name": "test2"}]
    mock_collection.find.return_value = documents

    result = get_data_from_collection(mock_db_instance, "test_collection")

    mock_db_instance.__getitem__.assert_called_once_with("test_collection")
    mock_collection.find.assert_called_once()
    assert result is not None
    assert isinstance(result[0], StringIO)
    assert result[1] == "raw-files/test_collection.json"
    expected_data = [{"name": "test1"}, {"name": "test2"}]
    assert json.loads(result[0].getvalue()) == expected_data
    mock_logger.info.assert_called_with("Extracting data from test_collection")
