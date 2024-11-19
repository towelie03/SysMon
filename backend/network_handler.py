import psutil
import time
import socket


class Network:
    @staticmethod
    def get_bandwidth_usage():
        """
        Returns the total bytes sent and received across all network
        """
        net_io = psutil.net_io_counters()
        return {
            "bytes_sent": net_io.bytes_sent,
            "bytes_received": net_io.bytes_recv,
            "packets_sent": net_io.packets_sent,
            "packets_received": net_io.packets_recv,
        }

    @staticmethod
    def bytes_convert(bytes_size):
        """
        Converts bytes to a human-readable format
        """
        units = ["B/s", "KB/s", "MB/s", "GB/s", "TB/s"]
        size = bytes_size
        unit = 0
        while size >= 1024 and unit < len(units) - 1:
            size /= 1024.0
            unit += 1
        return f"{size:.2f} {units[unit]}"

    @staticmethod
    def monitor_realtime_total_traffic(interval=1):
        """
        Continuously monitors and displays real-time total network traffic
        """
        print("Total Sent/s | Total Received/s")

        # Initial snapshot
        previous_net_io = psutil.net_io_counters()
        try:
            while True:
                time.sleep(interval)

                current_net_io = psutil.net_io_counters()

                # Calculate the total bytes per second
                sent_per_second = (
                    current_net_io.bytes_sent - previous_net_io.bytes_sent
                ) / interval
                recv_per_second = (
                    current_net_io.bytes_recv - previous_net_io.bytes_recv
                ) / interval

                sent_human = Network.bytes_convert(sent_per_second)
                recv_human = Network.bytes_convert(recv_per_second)

                print(f"{sent_human} {recv_human}")

                previous_net_io = current_net_io

        except KeyboardInterrupt:
            print("Real-time monitoring stopped.")

    @staticmethod
    def monitor_total_traffic(interval=1):
        previous_net_io = psutil.net_io_counters()
        time.sleep(interval)
        current_net_io = psutil.net_io_counters()
        sent_per_second = (
            current_net_io.bytes_sent - previous_net_io.bytes_sent
        ) / interval
        recv_per_second = (
            current_net_io.bytes_recv - previous_net_io.bytes_recv
        ) / interval
        monitored_traffic = {"sent": sent_per_second, "recv": recv_per_second}
        return monitored_traffic

    @staticmethod
    def get_primary_ipv4():
        hostname = socket.gethostname()
        ipv4_address = socket.gethostbyname(hostname)
        return ipv4_address

    @staticmethod
    def get_primary_ipv6():
        hostname = socket.gethostname()
        ipv6_info = socket.getaddrinfo(hostname, None, socket.AF_INET6)
        if ipv6_info:
            return ipv6_info[0][4][0]
        return None

    def get_primary_connection_type():
        connections = psutil.net_if_addrs()
        active_connections = psutil.net_if_stats()

        for interface in connections:
            if active_connections[interface].isup:  # Check if interface is active
                # Determine connection type based on naming conventions
                if "wlan" in interface or "Wi-Fi" in interface or "wifi" in interface:
                    return "WiFi"
                elif "eth" in interface or "en" in interface:
                    return "Ethernet"
                else:
                    return "Unknown"


def main():

    bandwidth = Network.get_bandwidth_usage()
    print(
        f"Total Bytes Sent: {bandwidth['bytes_sent']}, Total Bytes Received: {bandwidth['bytes_received']}"
    )
    Network.monitor_realtime_total_traffic(interval=1)


if __name__ == "__main__":
    main()
