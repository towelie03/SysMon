from unittest.mock import patch, Mock
from collections import deque
import pika
import json
from notification_client.notification_alert import (
    check_cpu,
    check_ram,
    check_network,
    send_alert,
)


@patch(
    "notification_client.notification_alert.cpu_usage_history",
    new_callable=lambda: deque(maxlen=5),
)
@patch("notification_client.notification_alert.fetch_cpu_usage")
@patch("notification_client.notification_alert.send_alert")
def test_high_cpu_alert(mock_send_alert, mock_fetch_cpu_usage, mock_cpu_usage_history):
    # Mock fetch_cpu_usage to return high CPU usage
    mock_fetch_cpu_usage.return_value = 90  # Single high value

    # Call check_cpu 5 times
    for _ in range(5):
        check_cpu()

    # Assert send_alert was called
    mock_send_alert.assert_called_once_with(
        "High CPU Usage", "CPU usage has been consistently high for the past 5 minutes"
    )

    # Assert that the mocked cpu_usage_history was updated
    assert list(mock_cpu_usage_history) == [90, 90, 90, 90, 90]
    assert mock_cpu_usage_history.maxlen == 5


@patch(
    "notification_client.notification_alert.ram_usage_history",
    new_callable=lambda: deque(maxlen=5),
)
@patch("notification_client.notification_alert.fetch_memory_percent")
@patch("notification_client.notification_alert.send_alert")
def test_high_ram_alert(
    mock_send_alert, mock_fetch_memory_percent, mock_ram_usage_history
):
    # Mock fetch_memory_percent to return high RAM usage
    mock_fetch_memory_percent.return_value = 92  # Single high value

    # Call check_ram 5 times
    for _ in range(5):
        check_ram()

    # Assert send_alert was called
    mock_send_alert.assert_called_once_with(
        "High RAM Usage", "RAM usage has been consistently high for the past 5 minutes"
    )

    # Assert that the mocked ram_usage_history was updated
    assert list(mock_ram_usage_history) == [92, 92, 92, 92, 92]
    assert mock_ram_usage_history.maxlen == 5


@patch("notification_client.notification_alert.fetch_network_bandwidth")
@patch("notification_client.notification_alert.send_alert")
def test_high_network_alert(mock_send_alert, mock_fetch_network_bandwidth):
    """
    Test that check_network triggers send_alert when a network spike is detected.
    """
    # Mock fetch_network_bandwidth to simulate a network spike
    mock_fetch_network_bandwidth.side_effect = [
        {"bytes_sent": 0, "bytes_received": 0},  # Initial stats
        {"bytes_sent": 200_000_000, "bytes_received": 100_000_000},  # Spike
    ]

    # Manually set initial values for prev_bytes_sent and prev_bytes_recv
    with patch("notification_client.notification_alert.prev_bytes_sent", 0), patch(
        "notification_client.notification_alert.prev_bytes_recv", 0
    ):
        # First call initializes prev_bytes_sent/prev_bytes_recv
        check_network()

        # Second call detects the spike
        check_network()

    # Assert send_alert was called
    mock_send_alert.assert_called_once_with(
        "High Network Usage", "Network spike detected"
    )


@patch("notification_client.notification_alert.pika.BlockingConnection")
@patch(
    "notification_client.notification_alert.time.strftime",
    return_value="2024-11-25 12:00:00",
)
def test_send_alert(mock_strftime, mock_blocking_connection):
    """
    Test the send_alert function to ensure it interacts with RabbitMQ correctly.
    """
    # Mock RabbitMQ connection and channel
    mock_connection = Mock()
    mock_channel = Mock()
    mock_blocking_connection.return_value = mock_connection
    mock_connection.channel.return_value = mock_channel

    # Call the function
    send_alert("High CPU Usage", "CPU usage exceeded 90% for 300s.")

    # Assert queue was declared
    mock_channel.queue_declare.assert_called_once_with(
        queue="alerts_queue", durable=True
    )

    # Assert message was published
    mock_channel.basic_publish.assert_called_once_with(
        exchange="",
        routing_key="alerts_queue",
        body=json.dumps(
            {
                "type": "High CPU Usage",
                "message": "CPU usage exceeded 90% for 300s.",
                "timestamp": "2024-11-25 12:00:00",
            }
        ),
        properties=pika.BasicProperties(delivery_mode=2),
    )

    # Assert connection was closed
    mock_connection.close.assert_called_once()

    # Verify correct print output
    with patch("builtins.print") as mock_print:
        send_alert("High CPU Usage", "CPU usage exceeded 90% for 5 minutes.")
        mock_print.assert_called_once_with(
            "Alert sent to queue: {'type': 'High CPU Usage', 'message': 'CPU usage exceeded 90% for 5 minutes.', 'timestamp': '2024-11-25 12:00:00'}"
        )
