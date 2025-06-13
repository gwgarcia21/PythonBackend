import pytest
import requests
from unittest.mock import patch
from .data_fetcher import fetch_data

@patch('data_fetcher.requests.get')
def test_fetch_data_success(mock_get):
  """Tests that fetch_data() returns the expected data on a successful API call."""
  mock_get.return_value.status_code = 200
  mock_get.return_value.json.return_value = {'key': 'value'}

  data = fetch_data('http://example.com/api')

  assert data == {'key': 'value'}
  mock_get.assert_called_once_with('http://example.com/api')

@patch('data_fetcher.requests.get')
def test_fetch_data_failure(mock_get):
    """Tests that fetch_data() raises an exception when the API call fails."""
    mock_get.return_value.status_code = 404
    mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError("Not Found")

    with pytest.raises(requests.exceptions.HTTPError):
        fetch_data('http://example.com/api')
    mock_get.assert_called_once_with('http://example.com/api')