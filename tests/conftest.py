"""Fixtures for module tests."""

from unittest.mock import MagicMock, patch

import pytest
from pymongo.collection import Collection
from pymongo.database import Database


@pytest.fixture
def mock_connection(mocker):
    """Fixture to mock MongoClient."""
    return mocker.patch("src.extract.extract.MongoClient")


@pytest.fixture
def mock_logger():
    with patch("src.extract.extract.logger") as mock:
        yield mock


@pytest.fixture
def mock_db():
    mock = MagicMock(spec=Database)
    mock_collection = MagicMock(spec=Collection)
    mock.__getitem__.return_value = mock_collection
    return mock, mock_collection
