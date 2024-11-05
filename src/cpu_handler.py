import psutil
import os
import uptime

class CPU:

    @staticmethod
    def get_cpu_usage(interval=1):
        """
        Returns the current overall CPU usage as a percentage.
        """
        return psutil.cpu_percent(interval=interval)
    
    @staticmethod
    def get_per_cpu_usage(interval=1):
        """
        Returns a list of CPU usage percentages per core.
        """
        return psutil.cpu_percent(interval=interval, percpu=True)
    
    @staticmethod
    def get_cpu_frequency():
        """
        Returns the current CPU frequency.
        """
        freq = psutil.cpu_freq()
        return {
            'current': freq.current,
            'min': freq.min,
            'max': freq.max
        }

    @staticmethod
    def get_cpu_count(logical=True):
        """
        Returns the number of logical or physical CPUs.
        """
        return psutil.cpu_count(logical=logical)

    @staticmethod
    def get_load_average():
        """
        Returns the load average over 1, 5, and 15 minutes.
        """
        return os.getloadavg()

    @staticmethod
    def get_core_utilization(interval=1):
        """
        Returns the utilization percentage of each CPU core.
        """
        return psutil.cpu_percent(interval=interval, percpu=True)

    @staticmethod
    def get_cpu_temperature():
        """
        Returns the CPU temperature if available.
        """
        # Source: PragmaticLinux
        # URL: https://www.pragmaticlinux.com/2020/06/check-the-raspberry-pi-cpu-temperature/
        result = 0.0
        if os.path.isfile('/sys/class/thermal/thermal_zone0/temp'):
            with open('/sys/class/thermal/thermal_zone0/temp') as f:
                line = f.readline().strip()
            # Test if the string is an integer as expected.
            if line.isdigit():
                # Convert the string with the CPU temperature to a float in degrees Celsius.
                result = float(line) / 1000
        return result

    @staticmethod
    def get_cpu_times():
        """
        Returns the time spent by the CPU in different modes.
        """
        return psutil.cpu_times()._asdict()

    @staticmethod
    def get_uptime():
        """
        Returns the system uptime in seconds.
        """
        return uptime.uptime()

def main():
    print("Overall CPU usage:")
    print(CPU.get_cpu_usage())

    print("\nPer-core CPU usage:")
    print(CPU.get_per_cpu_usage())

    print("\nCPU frequency:")
    print(CPU.get_cpu_frequency())

    print("\nLogical CPU count:")
    print(CPU.get_cpu_count(logical=True))

    print("\nPhysical CPU count:")
    print(CPU.get_cpu_count(logical=False))

    print("\nLoad average (1, 5, 15 minutes):")
    print(CPU.get_load_average())

    print("\nCore utilization:")
    print(CPU.get_core_utilization())

    print("\nCPU temperature:")
    print(CPU.get_cpu_temperature())

    print("\nCPU times:")
    print(CPU.get_cpu_times())

if __name__ == "__main__":
    main()
