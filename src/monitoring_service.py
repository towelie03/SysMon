# monitoring_service.py
import schedule
import time
import pika
import json
from cpu_handler import CPU
from mem_handler import Memory
from network_handler import Network
from collections import deque

# Monitoring parameters and RabbitMQ setup as before
monitoring_duration = 5 #5 * 60
check_interval = 5
high_cpu_threshold = 85
high_ram_threshold = 90
max_bandwidth_usage = 1e8

cpu_usage_history = deque(maxlen=monitoring_duration // check_interval)
ram_usage_history = deque(maxlen=monitoring_duration // check_interval)
prev_bytes_sent = Network.get_bandwidth_usage()["bytes_sent"]
prev_bytes_recv = Network.get_bandwidth_usage()["bytes_received"]

def send_alert(alert_type, message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='alerts_queue', durable=True)
    alert = {"type": alert_type, "message": message, "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")}
    channel.basic_publish(exchange='', routing_key='alerts_queue', body=json.dumps(alert),
                          properties=pika.BasicProperties(delivery_mode=2))
    print(f"Alert sent to queue: {alert}")
    connection.close()

def check_cpu():
    cpu_usage = CPU.get_cpu_usage()
    cpu_usage_history.append(cpu_usage)
    if len(cpu_usage_history) == cpu_usage_history.maxlen and all(usage > high_cpu_threshold for usage in cpu_usage_history):
        send_alert("High CPU Usage", f"CPU usage has been consistently high for the past 5 minutes")
        print("Sent high CPU alert")

def check_ram():
    ram_usage = Memory.get_memory_percent()
    ram_usage_history.append(ram_usage)
    if len(ram_usage_history) == ram_usage_history.maxlen and all(usage > high_ram_threshold for usage in ram_usage_history):
        send_alert("High RAM Usage", f"RAM usage has been consistently high for the past 5 minutes")
        print(f"Sent high RAM alert {ram_usage}")
def check_network():
    global prev_bytes_sent, prev_bytes_recv
    current_stats = Network.get_bandwidth_usage()
    sent_in_interval = current_stats["bytes_sent"] - prev_bytes_sent
    recv_in_interval = current_stats["bytes_received"] - prev_bytes_recv
    prev_bytes_sent, prev_bytes_recv = current_stats["bytes_sent"], current_stats["bytes_received"]
    if sent_in_interval > max_bandwidth_usage or recv_in_interval > max_bandwidth_usage:
        send_alert("High Network Usage", f"Network spike detected")
        print("Sent high Network alert")

schedule.every(check_interval).seconds.do(check_cpu)
schedule.every(check_interval).seconds.do(check_ram)
schedule.every(check_interval).seconds.do(check_network)

while True:
    schedule.run_pending()
    time.sleep(1)
