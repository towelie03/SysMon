import pytest
from unittest.mock import Mock, patch
from notification_client.notification_api_handler import fetch_cpu_usage, fetch_memory_percent, fetch_network_bandwidth


@patch("requests.get")
def test_fetch_cpu_usage(mock_requests_get):
    # Mock API response
    mock_requests_get.return_value = Mock(status_code=200, json=lambda: {"cpu_usage": 50})

    # Call fetch_cpu_usage
    result = fetch_cpu_usage()

    # Assert the correct value is returned
    assert result == 50


@patch("requests.get")
def test_fetch_memory_percent(mock_requests_get):
    # Mock API response
    mock_requests_get.return_value = Mock(status_code=200, json=lambda: {"memory_percent": 60})

    # Call fetch_memory_percent
    result = fetch_memory_percent()

    # Assert the correct value is returned
    assert result == 60


@patch("requests.get")
def test_fetch_network_bandwidth(mock_requests_get):
    # Mock API response
    mock_requests_get.return_value = Mock(
        status_code=200,
        json=lambda: {
            "bandwidth_usage": {"bytes_sent": 1000, "bytes_received": 2000}
        },
    )

    # Call fetch_network_bandwidth
    result = fetch_network_bandwidth()

    # Assert the correct values are returned
    assert result["bytes_sent"] == 1000
    assert result["bytes_received"] == 2000
