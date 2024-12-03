# monitoring_service.py
import schedule
import time
import pika
import json
import requests
from .notification_api_handler import (
    fetch_cpu_usage,
    fetch_memory_percent,
    fetch_network_bandwidth,
)
from collections import deque

# Default thresholds (fallback if the API call fails)
default_settings = {
    "high_cpu_threshold": 85,
    "high_ram_threshold": 90,
    "max_bandwidth_usage": 1e8,
    "check_interval": 5,
    "monitoring_duration": 5 * 60,
}

# Key mapping from API response to internal settings
key_mapping = {
    "cpu_threshold": "high_cpu_threshold",
    "memory_threshold": "high_ram_threshold",
    "network_threshold": "max_bandwidth_usage",
    "check_interval": "check_interval",
}

settings = default_settings.copy()

cpu_usage_history = deque(
    maxlen=settings["monitoring_duration"] // settings["check_interval"]
)
ram_usage_history = deque(
    maxlen=settings["monitoring_duration"] // settings["check_interval"]
)


def fetch_settings():
    global settings, cpu_usage_history, ram_usage_history
    try:
        response = requests.get("http://localhost:8000/settings")
        response.raise_for_status()
        updated_settings = response.json()

        # Map API keys to internal keys
        for api_key, internal_key in key_mapping.items():
            if api_key in updated_settings:
                if not settings[internal_key] == updated_settings[api_key]:
                    settings[internal_key] == updated_settings[api_key]

        # print(f"Settings updated: {settings}")

        # Reinitialize histories if check_interval or monitoring_duration changes
        cpu_usage_history = deque(
            maxlen=settings["monitoring_duration"] // settings["check_interval"]
        )
        ram_usage_history = deque(
            maxlen=settings["monitoring_duration"] // settings["check_interval"]
        )

    except Exception as e:
        print(f"Failed to fetch settings: {e}. Using default settings.")


# Fetch initial network statistics from the server
initial_bandwidth_stats = fetch_network_bandwidth()

if initial_bandwidth_stats is not None:
    prev_bytes_sent = initial_bandwidth_stats["bytes_sent"]
    prev_bytes_recv = initial_bandwidth_stats["bytes_received"]
else:
    # Fallback to zero if unable to fetch initial stats (to handle errors gracefully)
    prev_bytes_sent = 0
    prev_bytes_recv = 0


def send_alert(alert_type, message):
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="alerts_queue", durable=True)
    alert = {
        "type": alert_type,
        "message": message,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    channel.basic_publish(
        exchange="",
        routing_key="alerts_queue",
        body=json.dumps(alert),
        properties=pika.BasicProperties(delivery_mode=2),
    )
    print(f"Alert sent to queue: {alert}")
    connection.close()


def check_cpu():
    cpu_usage = fetch_cpu_usage()
    cpu_usage_history.append(cpu_usage)
    if len(cpu_usage_history) == cpu_usage_history.maxlen and all(
        usage > settings["high_cpu_threshold"] for usage in cpu_usage_history
    ):
        print(cpu_usage_history.maxlen)
        send_alert(
            "High CPU Usage",
            f"CPU usage has been consistently high for the past { settings['monitoring_duration'] }s",
        )
        print("Sent high CPU alert")


def check_ram():
    ram_usage = fetch_memory_percent()
    ram_usage_history.append(ram_usage)
    if len(ram_usage_history) == ram_usage_history.maxlen and all(
        usage > settings["high_ram_threshold"] for usage in ram_usage_history
    ):
        send_alert(
            "High RAM Usage",
            f"RAM usage has been consistently high for the past {settings['monitoring_duration'] }s",
        )
        print(f"Sent high RAM alert {ram_usage}")


def check_network():
    global prev_bytes_sent, prev_bytes_recv
    bandwidth_usage = fetch_network_bandwidth()
    if bandwidth_usage is not None:
        sent_in_interval = bandwidth_usage["bytes_sent"] - prev_bytes_sent
        recv_in_interval = bandwidth_usage["bytes_received"] - prev_bytes_recv
        prev_bytes_sent, prev_bytes_recv = (
            bandwidth_usage["bytes_sent"],
            bandwidth_usage["bytes_received"],
        )

        if (
            sent_in_interval > settings["max_bandwidth_usage"]
            or recv_in_interval > settings["max_bandwidth_usage"]
        ):
            send_alert("High Network Usage", "Network spike detected")
            print("Sent high network alert")
    else:
        print("Error: Unable to fetch network stats for this interval")


def start_monitoring():

    fetch_settings()

    schedule.every(settings["check_interval"]).seconds.do(check_cpu)
    schedule.every(settings["check_interval"]).seconds.do(check_ram)
    schedule.every(settings["check_interval"]).seconds.do(check_network)

    # Periodically refresh settings from the API
    schedule.every(60).seconds.do(fetch_settings)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    start_monitoring()
