import GPUtil
import subprocess


class GPU:

    @staticmethod
    def get_gpu_usage():
        """
        Returns the current overall GPU usage as a percentage.
        """
        gpus = GPUtil.getGPUs()
        if not gpus:
            return "No GPUs found."
        return {gpu.id: gpu.load * 100 for gpu in gpus}

    @staticmethod
    def get_gpu_memory_usage():
        """
        Returns the current GPU memory usage.
        """
        gpus = GPUtil.getGPUs()
        if not gpus:
            return "No GPUs found."
        return {
            gpu.id: {"used": gpu.memoryUsed, "total": gpu.memoryTotal} for gpu in gpus
        }

    @staticmethod
    def get_gpu_temperature():
        """
        Returns the current GPU temperature.
        """
        gpus = GPUtil.getGPUs()
        if not gpus:
            return "No GPUs found."
        return {gpu.id: gpu.temperature for gpu in gpus}

    @staticmethod
    def get_gpu_count():
        """
        Returns the number of GPUs.
        """
        gpus = GPUtil.getGPUs()
        return len(gpus)

    @staticmethod
    def get_gpu_details():
        """
        Returns details for each GPU.
        """
        gpus = GPUtil.getGPUs()
        if not gpus:
            return "No GPUs found."
        details = {}
        for gpu in gpus:
            details[gpu.id] = {
                "name": gpu.name,
                "load": gpu.load * 100,
                "memoryTotal": gpu.memoryTotal,
                "memoryUsed": gpu.memoryUsed,
                "temperature": gpu.temperature,
                "uuid": gpu.uuid,
            }
        return details

    @staticmethod
    def get_gpu_power_usage():
        """
        Returns the current power usage of each GPU in watts.
        """
        try:
            output = subprocess.check_output(
                [
                    "nvidia-smi",
                    "--query-gpu=power.draw",
                    "--format=csv,noheader,nounits",
                ]
            )
            power_usage = output.decode("utf-8").strip().split("\n")
            power_usage = [float(power) for power in power_usage]
            return {i: power for i, power in enumerate(power_usage)}
        except Exception as e:
            return str(e)


def main():
    print("Overall GPU usage:")
    print(GPU.get_gpu_usage())

    print("\nGPU memory usage:")
    print(GPU.get_gpu_memory_usage())

    print("\nGPU temperature:")
    print(GPU.get_gpu_temperature())

    print("\nGPU count:")
    print(GPU.get_gpu_count())

    print("\nGPU details:")
    print(GPU.get_gpu_details())

    print("\nGPU power usage:")
    print(GPU.get_gpu_power_usage())


if __name__ == "__main__":
    main()
