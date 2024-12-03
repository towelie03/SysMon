import asyncio
from .cpu_handler import CPU
from .mem_handler import Memory
from .disk_handler import Disk
from .network_handler import Network
from .nvidia_gpu_handler import GPU


class NotificationService:
    def __init__(self) -> None:
        self.cpu_threshold = 80
        self.memory_threshold = 80
        self.disk_threshold = 80
        self.network_threshold = 1000000
        self.gpu_threshold = 80
        self.check_interval = 10
        self.task = None
        self.listeners = []

    def add_listener(self, l):
        self.listeners.append(l)

    async def notify_listeners(self, title, msg):
        for i in self.listeners:
            await i(title, msg)


    async def event_loop(self):
        while True:
            await self.check_system_resources(
                self.cpu_threshold,
                self.memory_threshold,
                self.disk_threshold,
                self.network_threshold,
                self.gpu_threshold,
                self.check_interval,
            )
            await asyncio.sleep(self.check_interval)

    async def check_system_resources(
        self,
        cpu_threshold=80,
        memory_threshold=80,
        disk_threshold=80,
        network_threshold=1000000,
        gpu_threshold=80,
        check_interval=10,
    ):
        cpu_usage = CPU.get_cpu_usage()
        memory_usage = Memory.get_memory_percent()
        disk_usage = Disk.get_disk_usage("/")["percent"]
        net_io = Network.get_bandwidth_usage()
        network_usage = (
            net_io["bytes_sent"] + net_io["bytes_received"]
        ) / check_interval

        # Debugging: Print fetched values
        print(f"CPU Usage: {cpu_usage}")
        print(f"Memory Usage: {memory_usage}")
        print(f"Disk Usage: {disk_usage}")
        print(f"Network Usage: {Network.bytes_convert(network_usage)}")

        # Check CPU usage
        if cpu_usage > cpu_threshold:
            await self.notify_listeners("CPU Usage Alert", f"CPU usage is at {cpu_usage}%")
            print(f"CPU usage is above threshold: {cpu_usage}%")

        # Check Memory usage
        if memory_usage > memory_threshold:
            await self.notify_listeners("Memory Usage Alert", f"Memory usage is at {memory_usage:.2f}%")
            print(f"Memory usage is above threshold: {memory_usage:.2f}%")

        # Check Disk usage
        if disk_usage > disk_threshold:
            await self.notify_listeners("Disk Usage Alert", f"Disk usage is at {disk_usage}%")
            print(f"Disk usage is above threshold: {disk_usage}%")

        # Check Network usage
        # if network_usage > network_threshold:
        #     await self.notify_listeners("Network Usage Alert", f"Network usage is at {Network.bytes_convert(network_usage)}")
        #     print(
        #         f"Network usage is above threshold: {Network.bytes_convert(network_usage)}"
        #     )


    def start(self):
        self.stop()
        self.task = asyncio.create_task(self.event_loop())

    def stop(self):
        if self.task:
            self.task.cancel()


if __name__ == "__main__":
    async def run():
        service = NotificationService()
        service.start()

        await asyncio.sleep(10000)

    asyncio.run(run())
