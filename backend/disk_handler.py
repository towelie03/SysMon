import psutil
import time


class Disk:

    @staticmethod
    def get_disk_partitions():
        """
        Returns the disk partitions and their mount points.
        """
        partitions = psutil.disk_partitions()
        partition_info = []
        for partition in partitions:
            partition_info.append(
                {
                    "device": partition.device,
                    "mountpoint": partition.mountpoint,
                    "fstype": partition.fstype,
                    "opts": partition.opts,
                }
            )
        return partition_info

    @staticmethod
    def get_disk_usage(path="/"):
        """
        Returns the disk usage statistics (total, used, free space, and percentage).
        """
        usage = psutil.disk_usage(path)
        return {
            "total": usage.total,
            "used": usage.used,
            "free": usage.free,
            "percent": usage.percent,
        }

    @staticmethod
    def get_disk_io_counters():
        """
        Returns the input/output statistics such as the number of reads and writes.
        """
        io_counters = psutil.disk_io_counters()
        return {
            "read_count": io_counters.read_count,
            "write_count": io_counters.write_count,
            "read_bytes": io_counters.read_bytes,
            "write_bytes": io_counters.write_bytes,
            "read_time": io_counters.read_time,
            "write_time": io_counters.write_time,
        }

    @staticmethod
    def get_disk_io_counters_per_disk():
        """
        Returns the I/O statistics for each individual disk.
        """
        io_counters_per_disk = psutil.disk_io_counters(perdisk=True)
        return {disk: io._asdict() for disk, io in io_counters_per_disk.items()}

    @staticmethod
    def get_disk_active_time_percentage(interval=1):
        # Take the initial reading
        io_counters_start = psutil.disk_io_counters()
        start_time = time.time()

        # Wait for the specified interval
        time.sleep(interval)

        # Take the second reading
        io_counters_end = psutil.disk_io_counters()
        end_time = time.time()

        # Calculate active time in milliseconds over the interval
        read_time_diff = io_counters_end.read_time - io_counters_start.read_time
        write_time_diff = io_counters_end.write_time - io_counters_start.write_time
        active_time_diff = read_time_diff + write_time_diff

        # Calculate the interval duration in milliseconds
        interval_duration_ms = (end_time - start_time) * 1000

        # Calculate active time percentage
        active_time_percentage = (active_time_diff / interval_duration_ms) * 100
        return round(active_time_percentage, 2)


def main():
    print("Disk Partitions:")
    for partition in Disk.get_disk_partitions():
        print(partition)

    print("\nDisk Usage (Root partition):")
    print(Disk.get_disk_usage("/"))

    print("\nDisk I/O Counters:")
    print(Disk.get_disk_io_counters())

    print("\nDisk I/O Counters per Disk:")
    print(Disk.get_disk_io_counters_per_disk())
    # while(True):
    #     print("Disk Active Time")
    #     print(Disk.get_disk_active_time_percentage())


if __name__ == "__main__":
    main()
