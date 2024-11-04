from plyer import notification
import time
from src.cpu_handler import CPU
from src.mem_handler import Memory
from src.disk_handler import Disk
from src.network_handler import Network
from src.nvidia_gpu_handler import GPU

def check_system_resources(cpu_threshold=80, memory_threshold=80, disk_threshold=80, 
                           network_threshold=1000000, gpu_threshold=80, check_interval=10):
    while True:
        cpu_usage = CPU.get_cpu_usage()
        memory_usage = Memory.get_memory_usage()
        disk_usage = Disk.get_disk_usage('/')['percent']
        net_io = Network.get_bandwidth_usage()
        network_usage = (net_io['bytes_sent'] + net_io['bytes_received']) / check_interval
        
        gpu_usages = GPU.get_gpu_usage()  
        gpu_memory_usages = GPU.get_gpu_memory_usage()
        gpu_temperatures = GPU.get_gpu_temperature()  

        # Check CPU usage
        if cpu_usage > cpu_threshold:
            notification.notify(
                title='CPU Usage Alert',
                message=f'CPU usage is at {cpu_usage}%',
                timeout=10
            )

        # Check Memory usage
        if memory_usage > memory_threshold:
            notification.notify(
                title='Memory Usage Alert',
                message=f'Memory usage is at {memory_usage}%',
                timeout=10
            )

        # Check Disk usage
        if disk_usage > disk_threshold:
            notification.notify(
                title='Disk Usage Alert',
                message=f'Disk usage is at {disk_usage}%',
                timeout=10
            )

        # Check Network usage
        if network_usage > network_threshold:
            notification.notify(
                title='Network Usage Alert',
                message=f'Network usage is at {Network.bytes_convert(network_usage)}',
                timeout=10
            )

        # Check GPU usage and notify if any GPU exceeds the threshold
        for gpu_id, load in gpu_usages.items():
            if load > gpu_threshold:
                notification.notify(
                    title=f'GPU Usage Alert - GPU {gpu_id}',
                    message=f'GPU {gpu_id} usage is at {load:.2f}%',
                    timeout=10
                )
        
        # Check GPU memory usage
        for gpu_id, mem_info in gpu_memory_usages.items():
            used_memory_percentage = (mem_info['used'] / mem_info['total']) * 100
            if used_memory_percentage > gpu_threshold:
                notification.notify(
                    title=f'GPU Memory Usage Alert - GPU {gpu_id}',
                    message=f'GPU {gpu_id} memory usage is at {used_memory_percentage:.2f}%',
                    timeout=10
                )

        # Check GPU temperature
        for gpu_id, temp in gpu_temperatures.items():
            if temp > 80:
                notification.notify(
                    title=f'GPU Temperature Alert - GPU {gpu_id}',
                    message=f'GPU {gpu_id} temperature is at {temp}°C',
                    timeout=10
                )

        time.sleep(check_interval)

if __name__ == "__main__":
    check_system_resources(cpu_threshold=80, memory_threshold=80, 
                           disk_threshold=80, network_threshold=1000000, 
                           gpu_threshold=80, check_interval=10)

