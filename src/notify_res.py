from plyer import notification
import asyncio
from collections import deque
import psutil  # Import psutil for disk I/O
from cpu_handler import CPU
from mem_handler import Memory
from disk_handler import Disk
from network_handler import Network
from nvidia_gpu_handler import GPU


async def check_system_resources(cpu_threshold=80, memory_threshold=80, storage_threshold=90,
                                 gpu_threshold=80, disk_io_threshold=100, check_interval=10):
    # Queue to store recent network usage values for rolling average
    network_usage_history = deque(maxlen=5)  # Track last 5 intervals

    # Initial disk I/O counters to calculate throughput
    old_io = psutil.disk_io_counters()

    while True:
        # Get CPU, memory, disk storage usage
        cpu_usage = CPU.get_cpu_usage()
        memory_usage = Memory.get_memory_percent()
        disk_storage_usage = Disk.get_disk_usage('/')['percent']  # Storage as percentage
        net_io = Network.get_bandwidth_usage()
        network_usage = (net_io['bytes_sent'] + net_io['bytes_received']) / check_interval

        gpu_usages = GPU.get_gpu_usage()
        gpu_memory_usages = GPU.get_gpu_memory_usage()
        gpu_temperatures = GPU.get_gpu_temperature()

        # Disk I/O throughput calculation
        new_io = psutil.disk_io_counters()
        read_speed = (new_io.read_bytes - old_io.read_bytes) / check_interval
        write_speed = (new_io.write_bytes - old_io.write_bytes) / check_interval
        total_speed = (read_speed + write_speed) / (1024 * 1024)  # Convert to MB/s
        old_io = new_io  # Update old_io for the next interval

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
        if total_speed > disk_io_threshold:  # Threshold for disk I/O throughput in MB/s
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

        # # Check GPU usage and notify if any GPU exceeds the threshold
        # for gpu_id, load in gpu_usages.items():
        #     if load > gpu_threshold:
        #         print(f"GPU {gpu_id} usage is above threshold: {load:.2f}%")
        #         notification.notify(
        #             title=f'GPU Usage Alert - GPU {gpu_id}',
        #             message=f'GPU {gpu_id} usage is at {load:.2f}%',
        #             timeout=10
        #         )

        # # Check GPU memory usage
        # for gpu_id, mem_info in gpu_memory_usages.items():
        #     used_memory_percentage = (mem_info['used'] / mem_info['total']) * 100
        #     if used_memory_percentage > gpu_threshold:
        #         print(f"GPU {gpu_id} memory usage is above threshold: {used_memory_percentage:.2f}%")
        #         notification.notify(
        #             title=f'GPU Memory Usage Alert - GPU {gpu_id}',
        #             message=f'GPU {gpu_id} memory usage is at {used_memory_percentage:.2f}%',
        #             timeout=10
        #         )

        # # Check GPU temperature
        # for gpu_id, temp in gpu_temperatures.items():
        #     if temp > 80:
        #         print(f"GPU {gpu_id} temperature is above threshold: {temp}°C")
        #         notification.notify(
        #             title=f'GPU Temperature Alert - GPU {gpu_id}',
        #             message=f'GPU {gpu_id} temperature is at {temp}°C',
        #             timeout=10
        #         )

        await asyncio.sleep(check_interval)


if __name__ == "__main__":
    asyncio.run(check_system_resources(cpu_threshold=80, memory_threshold=75,
                                       storage_threshold=90, gpu_threshold=80,
                                       disk_io_threshold=100, check_interval=10))
