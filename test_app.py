"""tests for the app.py"""

import pytest
from app import app
from unittest.mock import patch
import requests

@pytest.fixture
def client():
    """Fixture to create a test client for the Flask app."""
    with app.test_client() as client:
        yield client

def test_version_endpoint(client):
    """Test the /version endpoint for correct response."""
    response = client.get('/version')
    assert response.status_code == 200
    assert response.json == {"version": "0.0.1"}

@patch('app.requests.get')
def test_temperature_endpoint_success(mock_get, client):
    """Test the /temperature endpoint for success scenario."""
    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response._content = b'{"sensors":[{"title":"Temperatur","lastMeasurement":{"value":"20.0","createdAt":"2021-01-01T01:00:00.000Z"}}]}'
    mock_get.return_value = mock_response

    response = client.get('/temperature')
    assert response.status_code == 200
    assert "average_temperature" in response.json

@patch('app.requests.get')
def test_temperature_endpoint_failure(mock_get, client):
    """Test the /temperature endpoint for failure scenario."""
    mock_get.side_effect = requests.exceptions.RequestException()

    response = client.get('/temperature')
    assert response.status_code == 500
