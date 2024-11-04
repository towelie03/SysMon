import psutil
from plyer import notification
import time
from src.cpu_handler import CPU 
from src.mem_handler import Memory
from src.disk_handler import Disk
from src.network_handler import Network

def check_system_resources(cpu_threshold=80, memory_threshold=80, disk_threshold=80, network_threshold=1000000, check_interval=10):
    while True:
        cpu_usage = CPU.get_cpu_usage()
        memory_usage = Memory.get_memory_usage()
        disk_usage = Disk.get_disk_usage('/')['percent'] 
        net_io = Network.get_bandwidth_usage()
        network_usage = (net_io['bytes_sent'] + net_io['bytes_received']) / check_interval

        if cpu_usage > cpu_threshold:
            notification.notify(
                title='CPU Usage Alert',
                message=f'CPU usage is at {cpu_usage}%',
                timeout=10
            )

        if memory_usage > memory_threshold:
            notification.notify(
                title='Memory Usage Alert',
                message=f'Memory usage is at {memory_usage}%',
                timeout=10
            )

        if disk_usage > disk_threshold:
            notification.notify(
                title='Disk Usage Alert',
                message=f'Disk usage is at {disk_usage}%',
                timeout=10
            )

        if network_usage > network_threshold:
            notification.notify(
                title='Network Usage Alert',
                message=f'Network usage is at {Network.bytes_convert(network_usage)}',
                timeout=10
            )

        time.sleep(check_interval)

if __name__ == "__main__":
    check_system_resources(cpu_threshold=80, memory_threshold=80, disk_threshold=80, network_threshold=1000000, check_interval=10)
