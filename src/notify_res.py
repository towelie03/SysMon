from plyer import notification
import asyncio
from collections import deque
import psutil
from datetime import datetime
from cpu_handler import CPU
from mem_handler import Memory
from disk_handler import Disk
from network_handler import Network
from nvidia_gpu_handler import GPU


def get_disk_type_and_threshold():
    thresholds = {
        'hdd': 100,
        'sata_ssd': 300,
        'nvme_ssd': 1000
    }

    disk_type = 'unknown'
    for disk in psutil.disk_partitions():
        if 'nvme' in disk.device:
            disk_type = 'nvme_ssd'
            break
        elif 'sd' in disk.device:
            disk_type = 'sata_ssd'
        elif 'hd' in disk.device:
            disk_type = 'hdd'

    disk_io_threshold = thresholds.get(disk_type, 100)
    print(f"Detected Disk Type: {disk_type}")
    print(f"Disk I/O Threshold set to: {disk_io_threshold} MB/s")
    return disk_io_threshold


def check_gpu_availability():
    gpu_info = GPU.get_gpu_usage()
    if isinstance(gpu_info, dict) and gpu_info:
        print("GPU detected. Monitoring enabled.")
        return True
    else:
        print("No GPU detected. GPU monitoring disabled.")
        return False


async def check_system_resources(cpu_threshold=80, memory_threshold=80, storage_threshold=90,
                                 gpu_threshold=80, disk_io_threshold=100, check_interval=10):
    network_usage_history = deque(maxlen=5)
    old_io = psutil.disk_io_counters()
    has_gpu = check_gpu_availability()
    interval_count = 1

    while True:
        # Timestamp and elapsed time
        elapsed_time = interval_count * check_interval
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"\nInterval {interval_count}: {elapsed_time} sec (Timestamp: {timestamp})\n")

        # Initialize alert summary
        alerts = []

        # System metrics
        cpu_usage = CPU.get_cpu_usage()
        memory_usage = Memory.get_memory_percent()
        disk_storage_usage = Disk.get_disk_usage('/')['percent']
        net_io = Network.get_bandwidth_usage()
        network_usage = (net_io['bytes_sent'] + net_io['bytes_received']) / (1024 * 1024 * check_interval)

        gpu_usages = GPU.get_gpu_usage() if has_gpu else {}
        gpu_memory_usages = GPU.get_gpu_memory_usage() if has_gpu else {}
        gpu_temperatures = GPU.get_gpu_temperature() if has_gpu else {}

        if not isinstance(gpu_usages, dict): gpu_usages = {}
        if not isinstance(gpu_memory_usages, dict): gpu_memory_usages = {}
        if not isinstance(gpu_temperatures, dict): gpu_temperatures = {}

        new_io = psutil.disk_io_counters()
        read_speed = (new_io.read_bytes - old_io.read_bytes) / (1024 * 1024 * check_interval)
        write_speed = (new_io.write_bytes - old_io.write_bytes) / (1024 * 1024 * check_interval)
        total_speed = read_speed + write_speed
        old_io = new_io

        network_usage_history.append(network_usage)
        avg_network_usage = sum(network_usage_history) / len(network_usage_history)
        dynamic_network_threshold = avg_network_usage * 1.2

        # Function to print and notify alerts
        def print_and_notify(name, value, unit, threshold):
            if value > threshold:
                alerts.append(name)
                print(f"{name}: {value:.2f} {unit} ***ALERT***")
                notification.notify(
                    title=f"{name} Alert",
                    message=f"{name} has reached {value:.2f} {unit}, which is above the threshold!",
                    timeout=10
                )
            else:
                print(f"{name}: {value:.2f} {unit}")

        # Check and notify for each metric
        print_and_notify("CPU Usage", cpu_usage, "%", cpu_threshold)
        print_and_notify("Memory Usage", memory_usage, "%", memory_threshold)
        print_and_notify("Disk Storage Usage", disk_storage_usage, "%", storage_threshold)
        print_and_notify("Disk I/O Throughput", total_speed, "MB/s", disk_io_threshold)
        print_and_notify("Network Usage", network_usage, "MB/s", dynamic_network_threshold)
        print(f"Dynamic Network Threshold: {dynamic_network_threshold:.2f} MB/s")

        if has_gpu:
            for gpu_id, load in gpu_usages.items():
                print_and_notify(f"GPU {gpu_id} Usage", load, "%", gpu_threshold)
            for gpu_id, mem_info in gpu_memory_usages.items():
                used_memory_percentage = (mem_info['used'] / mem_info['total']) * 100
                print_and_notify(f"GPU {gpu_id} Memory Usage", used_memory_percentage, "%", gpu_threshold)
            for gpu_id, temp in gpu_temperatures.items():
                if temp > 80:
                    alerts.append(f"GPU {gpu_id} Temperature")
                    print(f"GPU {gpu_id} Temperature: {temp}°C ***ALERT***")
                    notification.notify(
                        title=f"GPU {gpu_id} Temperature Alert",
                        message=f"GPU {gpu_id} temperature is at {temp}°C, which is above the threshold!",
                        timeout=10
                    )
                else:
                    print(f"GPU {gpu_id} Temperature: {temp}°C")

        # Summary
        if alerts:
            print(f"\nSummary: Alerts - {', '.join(alerts)}")
        else:
            print("\nSummary: No alerts")

        print("\n------------------------------------------------")
        interval_count += 1
        await asyncio.sleep(check_interval)


if __name__ == "__main__":
    disk_io_threshold = get_disk_type_and_threshold()
    asyncio.run(check_system_resources(cpu_threshold=80, memory_threshold=75,
                                       storage_threshold=90, gpu_threshold=80,
                                       disk_io_threshold=disk_io_threshold, check_interval=10))
