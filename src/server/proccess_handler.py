import psutil
from datetime import datetime

class Process:

    def bytes_to_human(bytes_size):
        """
        Converts bytes to a human-readable format (KB, MB, GB).
        """
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        size = bytes_size
        unit = 0
        while size >= 1024 and unit < len(units) - 1:
            size /= 1024.0
            unit += 1
        return f"{size:.2f} {units[unit]}"

    @staticmethod
    def list_all_processes():
        """
        Lists all running processes with their details.
        """
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 'memory_info', 'create_time']):
            try:
                # Fetch information about each process
                process_info = {
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'status': proc.info['status'],
                    'cpu_usage': proc.info['cpu_percent'],
                    'memory_usage': Process.bytes_to_human(proc.info['memory_info'].rss),
                    'start_time': datetime.fromtimestamp(proc.info['create_time']).strftime("%Y-%m-%d %H:%M:%S")
                }
                processes.append(process_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue  # Handle processes that have exited or are not accessible
        return processes
    
    @staticmethod
    def get_process_info(pid):
        """
        Retrieves and returns key process information.
        """
        process = psutil.Process(pid)
        try:
            process_info = {
                'pid': process.pid,
                'name':process.name(),
                'status':process.status(),
                'cpu_usage':process.cpu_percent(interval=1.0),
                'memory_usage':Process.bytes_to_human(process.memory_info().rss),
                'start_time': datetime.fromtimestamp(process.create_time()).strftime("%Y-%m-%d %H:%M:%S")
            }
            return process_info
        except psutil.NoSuchProcess:
            return None
    

def main():
    all_processes = Process.list_all_processes()
    for process in all_processes:
        print(f"PID: {process['pid']}, Name: {process['name']}, Status: {process['status']}, "
              f"CPU: {process['cpu_usage']}%, Memory: {process['memory_usage']}, "
              f"Started: {process['start_time']}")

    process = Process.get_process_info(1)
    print(f"PID: {process['pid']}, Name: {process['name']}, Status: {process['status']}, "
              f"CPU: {process['cpu_usage']}%, Memory: {process['memory_usage']}, "
              f"Started: {process['start_time']}")
