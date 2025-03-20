"""Fixtures for module tests."""

import pytest


@pytest.fixture
def mock_connection(mocker):
    """Fixture to mock MongoClient."""
    return mocker.patch("src.extract.extract.MongoClient")
