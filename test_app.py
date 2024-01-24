# pylint: disable=redefined-outer-name

"""Module for testing app.py endpoints."""

from unittest.mock import patch
from datetime import datetime
import pytest
import requests
from app import app


@pytest.fixture
def test_client():
    """Fixture to create a test client for the Flask app."""
    with app.test_client() as client:
        yield client

def test_version_endpoint(test_client):
    """Test the /version endpoint for correct response."""
    response = test_client.get('/version')
    assert response.status_code == 200
    assert response.json == {"version": "0.0.1"}

@patch('app.requests.get')
def test_temperature_endpoint_success(mock_get, test_client):
    """Test the /temperature endpoint for success scenario."""
    mock_data = {
        "sensors": [
            {
                "title": "Temperatur",
                "lastMeasurement": {
                    "value": "20.0",
                    "createdAt": datetime.utcnow().isoformat() + "Z" 
                }
            }
            # Include other sensors if necessary
        ]
    }
    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response.json = lambda: mock_data
    mock_get.return_value = mock_response

    response = test_client.get('/temperature')
    assert response.status_code == 200
    assert "average_temperature" in response.json

@patch('app.requests.get')
def test_temperature_endpoint_failure(mock_get, test_client):
    """Test the /temperature endpoint for failure scenario."""
    mock_get.side_effect = requests.exceptions.RequestException()

    response = test_client.get('/temperature')
    assert response.status_code == 500
