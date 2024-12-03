import os
import json
from unittest.mock import patch, Mock

# Set environment variables before importing dependent modules
os.environ["RECEIVER_EMAIL"] = "mock_receiver@example.com"

# Import after environment setup
from notification_client.email_alert import send_email_alert, callback  # noqa: E402


@patch("notification_client.email_alert.SMTP_SERVER", "mock.smtp.server")
@patch("notification_client.email_alert.SMTP_PORT", 1025)
@patch("notification_client.email_alert.SENDER_EMAIL", "mock_sender@example.com")
@patch("notification_client.email_alert.SENDER_PASSWORD", "mock_password")
@patch("notification_client.email_alert.RECEIVER_EMAIL", "mock_receiver@example.com")
@patch("notification_client.email_alert.smtplib.SMTP")
def test_send_email_alert(mock_smtp):
    """
    Test the send_email_alert function to ensure it sends an email correctly with mocked configuration.
    """
    # Mock SMTP server behavior
    mock_server = mock_smtp.return_value.__enter__.return_value

    # Call the function
    send_email_alert("Test Subject", "Test Message", "mock_receiver@example.com")

    # Verify SMTP methods were called correctly
    mock_smtp.assert_called_once_with("mock.smtp.server", 1025)
    mock_server.starttls.assert_called_once()
    mock_server.login.assert_called_once_with(
        "mock_sender@example.com", "mock_password"
    )
    mock_server.sendmail.assert_called_once_with(
        "mock_sender@example.com",
        "mock_receiver@example.com",
        'Content-Type: text/plain; charset="us-ascii"\n'
        "MIME-Version: 1.0\n"
        "Content-Transfer-Encoding: 7bit\n"
        "Subject: Test Subject\n"
        "From: mock_sender@example.com\n"
        "To: mock_receiver@example.com\n\n"
        "Test Message",
    )


@patch("notification_client.email_alert.SMTP_SERVER", "mock.smtp.server")
@patch("notification_client.email_alert.SMTP_PORT", 1025)
@patch("notification_client.email_alert.SENDER_EMAIL", "mock_sender@example.com")
@patch("notification_client.email_alert.SENDER_PASSWORD", "mock_password")
@patch("notification_client.email_alert.RECEIVER_EMAIL", "mock_receiver@example.com")
@patch("notification_client.email_alert.send_email_alert")
def test_callback(mock_send_email_alert):
    """
    Test the callback function to ensure it processes RabbitMQ messages correctly with mocked configuration.
    """
    # Mock RabbitMQ delivery and message
    mock_channel = Mock()
    mock_method = Mock()
    mock_properties = Mock()
    mock_body = json.dumps(
        {
            "type": "High CPU Usage",
            "message": "CPU usage exceeded 90% for 5 minutes.",
            "timestamp": "2024-11-25 12:00:00",
        }
    ).encode()

    # Call the function
    callback(mock_channel, mock_method, mock_properties, mock_body)

    # Verify send_email_alert was called with correct arguments
    mock_send_email_alert.assert_called_once_with(
        "System Alert: High CPU Usage",
        "Time: 2024-11-25 12:00:00\n\nAlert: High CPU Usage\n\nDetails: CPU usage exceeded 90% for 5 minutes.",
        "mock_receiver@example.com",
    )

    # Verify message was acknowledged
    mock_channel.basic_ack.assert_called_once_with(
        delivery_tag=mock_method.delivery_tag
    )
