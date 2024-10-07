import psutil

class Network:
    @staticmethod
    def get_bandwidth_usage():
        """
        Returns the total bytes sent and received across all network
        """
        net_io = psutil.net_io_counters()
        return {
            'bytes_sent': net_io.bytes_sent,
            'bytes_received': net_io.bytes_recv,
            'packets_sent': net_io.packets_sent,
            'packets_received': net_io.packets_recv
        }

def main():

    bandwidth = Network.get_bandwidth_usage()
    print(f"Total Bytes Sent: {bandwidth['bytes_sent']}, Total Bytes Received: {bandwidth['bytes_received']}")

if __name__ == "__main__":
    main()