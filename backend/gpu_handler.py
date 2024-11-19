import GPUtil
import os
import subprocess

class GPU:

    @staticmethod
    def _check_gpus():
        """
        Checks if GPUs are available. Returns True if found, False otherwise.
        """
        gpus = GPUtil.getGPUs()
        return gpus if gpus else None

    @staticmethod
    def get_gpu_usage():
        """
        Returns the current overall GPU usage as a percentage.
        """
        gpus = GPU._check_gpus()
        if gpus is None:
            return "No GPUs found."
        return {gpu.id: gpu.load * 100 for gpu in gpus}

    @staticmethod
    def get_gpu_memory_usage():
        """
        Returns the current GPU memory usage.
        """
        gpus = GPU._check_gpus()
        if gpus is None:
            return "No GPUs found."
        return {gpu.id: {'used': gpu.memoryUsed, 'total': gpu.memoryTotal} for gpu in gpus}

    @staticmethod
    def get_gpu_temperature():
        """
        Returns the current GPU temperature.
        """
        gpus = GPU._check_gpus()
        if gpus is None:
            return "No GPUs found."
        return {gpu.id: gpu.temperature for gpu in gpus}

    @staticmethod
    def get_gpu_count():
        """
        Returns the number of GPUs.
        """
        gpus = GPU._check_gpus()
        return len(gpus) if gpus else 0

    @staticmethod
    def get_gpu_details():
        """
        Returns details for each GPU.
        """
        gpus = GPU._check_gpus()
        if gpus is None:
            return "No GPUs found."
        details = {}
        for gpu in gpus:
            details[gpu.id] = {
                'name': gpu.name,
                'load': gpu.load * 100,
                'memoryTotal': gpu.memoryTotal,
                'memoryUsed': gpu.memoryUsed,
                'temperature': gpu.temperature,
                'uuid': gpu.uuid
            }
        return details

    @staticmethod
    def get_gpu_power_usage():
        """
        Returns the current power usage of each GPU in watts.
        """
        try:
            output = subprocess.check_output(
                ["nvidia-smi", "--query-gpu=power.draw", "--format=csv,noheader,nounits"]
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

