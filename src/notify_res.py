from plyer import notification
import asyncio
from collections import deque
import psutil
from cpu_handler import CPU
from mem_handler import Memory
from disk_handler import Disk
from network_handler import Network
from nvidia_gpu_handler import GPU

def get_disk_type_and_threshold():
    # Default threshold values (in MB/s) based on disk type, could be more optimized.
    thresholds = {
        'hdd': 100,
        'sata_ssd': 300,
        'nvme_ssd': 1000
    }

    # Detect disk type by inspecting disk device names
    disk_type = 'unknown'
    for disk in psutil.disk_partitions():
        if 'nvme' in disk.device:
            disk_type = 'nvme_ssd'
            break
        elif 'sd' in disk.device:
            # Assuming SATA SSD if it’s /dev/sdX
            disk_type = 'sata_ssd'
        elif 'hd' in disk.device:
            # Assuming HDD if it’s /dev/hdX
            disk_type = 'hdd'

    # Get threshold based on detected disk type, default to 100 MB/s if unknown. Might need to be higher.
    disk_io_threshold = thresholds.get(disk_type, 100)

    print(f"Detected Disk Type: {disk_type}")
    print(f"Disk I/O Threshold set to: {disk_io_threshold} MB/s")
    return disk_io_threshold

def check_gpu_availability():
    # Check if any GPU information is available
    gpu_info = GPU.get_gpu_usage()
    if isinstance(gpu_info, dict) and gpu_info:  # Ensure it's a non-empty dictionary
        print("GPU detected. Monitoring enabled.")
        return True
    else:
        print("No GPU detected. GPU monitoring disabled.")
        return False

async def check_system_resources(cpu_threshold=80, memory_threshold=80, storage_threshold=90,
                                 gpu_threshold=80, disk_io_threshold=100, check_interval=10):
    # Queue to store recent network usage values for rolling average, tracking last 5 intervals
    network_usage_history = deque(maxlen=5)

    # Initial disk I/O counters to calculate throughput
    old_io = psutil.disk_io_counters()

    # Determine GPU availability
    has_gpu = check_gpu_availability()

    while True:
        # Get CPU, memory, disk storage usage
        cpu_usage = CPU.get_cpu_usage()
        memory_usage = Memory.get_memory_percent()
        disk_storage_usage = Disk.get_disk_usage('/')['percent']
        net_io = Network.get_bandwidth_usage()
        network_usage = (net_io['bytes_sent'] + net_io['bytes_received']) / check_interval

        # Only retrieve GPU data if a GPU is detected
        gpu_usages = GPU.get_gpu_usage() if has_gpu else {}
        gpu_memory_usages = GPU.get_gpu_memory_usage() if has_gpu else {}
        gpu_temperatures = GPU.get_gpu_temperature() if has_gpu else {}

        # Ensure GPU data is a dictionary, otherwise set it to empty if unavailable
        if not isinstance(gpu_usages, dict):
            gpu_usages = {}
        if not isinstance(gpu_memory_usages, dict):
            gpu_memory_usages = {}
        if not isinstance(gpu_temperatures, dict):
            gpu_temperatures = {}

        # Disk I/O throughput calculation
        new_io = psutil.disk_io_counters()
        read_speed = (new_io.read_bytes - old_io.read_bytes) / check_interval
        write_speed = (new_io.write_bytes - old_io.write_bytes) / check_interval
        # Convert to MB/s
        total_speed = (read_speed + write_speed) / (1024 * 1024)
        # Update old_io for the next interval
        old_io = new_io

        # Add current network usage to the history for rolling average calculation
        network_usage_history.append(network_usage)

        # Calculate the rolling average for network usage
        avg_network_usage = sum(network_usage_history) / len(network_usage_history)

        # Set the dynamic network threshold as 20% above the average
        dynamic_network_threshold = avg_network_usage * 1.2

        # Debugging: Print fetched values and dynamic threshold
        print(f"CPU Usage: {cpu_usage}")
        print(f"Memory Usage: {memory_usage}")
        print(f"Disk Storage Usage: {disk_storage_usage}%")
        print(f"Disk I/O Throughput: {total_speed:.2f} MB/s")
        print(f"Network Usage: {Network.bytes_convert(network_usage)}")
        print(f"Dynamic Network Threshold: {Network.bytes_convert(dynamic_network_threshold)}")
        if has_gpu:
            print(f"GPU Usages: {gpu_usages}")
            print(f"GPU Memory Usages: {gpu_memory_usages}")
            print(f"GPU Temperatures: {gpu_temperatures}")

        # Check CPU usage
        if cpu_usage > cpu_threshold:
            print(f"CPU usage is above threshold: {cpu_usage}%")
            notification.notify(
                title='CPU Usage Alert',
                message=f'CPU usage is at {cpu_usage}%',
                timeout=10
            )

        # Check Memory usage
        if memory_usage > memory_threshold:
            print(f"Memory usage is above threshold: {memory_usage:.2f}%")
            notification.notify(
                title='Memory Usage Alert',
                message=f'Memory usage is at {memory_usage:.2f}%',
                timeout=10
            )

        # Check Disk Storage usage
        if disk_storage_usage > storage_threshold:
            print(f"Disk storage usage is above threshold: {disk_storage_usage}%")
            notification.notify(
                title='Disk Storage Alert',
                message=f'Disk storage usage is at {disk_storage_usage}%',
                timeout=10
            )

        # Check Disk I/O throughput
        if total_speed > disk_io_threshold:
            print(f"Disk I/O is above threshold: {total_speed:.2f} MB/s")
            notification.notify(
                title='Disk I/O Alert',
                message=f'Disk I/O throughput is at {total_speed:.2f} MB/s',
                timeout=10
            )

        # Check Network usage using the dynamic threshold
        if network_usage > dynamic_network_threshold:
            print(f"Network usage is above dynamic threshold: {Network.bytes_convert(network_usage)}")
            notification.notify(
                title='Network Usage Alert',
                message=f'Network usage is at {Network.bytes_convert(network_usage)}',
                timeout=10
            )

        # GPU monitoring, only if GPU is available
        if has_gpu:
            # Check GPU usage
            for gpu_id, load in gpu_usages.items():
                if load > gpu_threshold:
                    print(f"GPU {gpu_id} usage is above threshold: {load:.2f}%")
                    notification.notify(
                        title=f'GPU Usage Alert - GPU {gpu_id}',
                        message=f'GPU {gpu_id} usage is at {load:.2f}%',
                        timeout=10
                    )

            # Check GPU memory usage
            for gpu_id, mem_info in gpu_memory_usages.items():
                used_memory_percentage = (mem_info['used'] / mem_info['total']) * 100
                if used_memory_percentage > gpu_threshold:
                    print(f"GPU {gpu_id} memory usage is above threshold: {used_memory_percentage:.2f}%")
                    notification.notify(
                        title=f'GPU Memory Usage Alert - GPU {gpu_id}',
                        message=f'GPU {gpu_id} memory usage is at {used_memory_percentage:.2f}%',
                        timeout=10
                    )

            # Check GPU temperature
            for gpu_id, temp in gpu_temperatures.items():
                if temp > 80:
                    print(f"GPU {gpu_id} temperature is above threshold: {temp}°C")
                    notification.notify(
                        title=f'GPU Temperature Alert - GPU {gpu_id}',
                        message=f'GPU {gpu_id} temperature is at {temp}°C',
                        timeout=10
                    )

        await asyncio.sleep(check_interval)


if __name__ == "__main__":
    # Automatically set disk_io_threshold based on disk type
    disk_io_threshold = get_disk_type_and_threshold()

    asyncio.run(check_system_resources(cpu_threshold=80, memory_threshold=75,
                                       storage_threshold=90, gpu_threshold=80,
                                       disk_io_threshold=disk_io_threshold, check_interval=10))
