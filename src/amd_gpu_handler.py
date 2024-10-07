import pyamdgpuinfo
import subprocess

class AMDGPU:
    
    @staticmethod
    def _check_gpus():
        """
        Checks if AMD GPUs are available. Returns a list of devices or None.
        """
        devices = pyamdgpuinfo.get_gpu()
        return devices if devices else None

    @staticmethod
    def get_gpu_usage():
        """
        Returns the current overall GPU usage as a percentage.
        """
        gpus = AMDGPU._check_gpus()
        if gpus is None:
            return "No AMD GPUs found."
        
        usage = {}
        for device in gpus:
            usage[device.id] = device.activity * 100  # Activity is a float [0.0 - 1.0]
        return usage

    @staticmethod
    def get_gpu_temperature():
        """
        Returns the current GPU temperature.
        """
        gpus = AMDGPU._check_gpus()
        if gpus is None:
            return "No AMD GPUs found."
        
        temperatures = {}
        for device in gpus:
            temperatures[device.id] = device.temperature
        return temperatures

    @staticmethod
    def get_gpu_memory_usage():
        """
        Returns the current GPU memory usage.
        """
        gpus = AMDGPU._check_gpus()
        if gpus is None:
            return "No AMD GPUs found."
        
        memory_usage = {}
        for device in gpus:
            memory_usage[device.id] = {
                'used': device.memory_used,
                'total': device.memory_total
            }
        return memory_usage

    @staticmethod
    def get_gpu_count():
        """
        Returns the number of AMD GPUs.
        """
        gpus = AMDGPU._check_gpus()
        return len(gpus) if gpus else 0

    @staticmethod
    def get_gpu_details():
        """
        Returns details for each AMD GPU.
        """
        gpus = AMDGPU._check_gpus()
        if gpus is None:
            return "No AMD GPUs found."
        
        details = {}
        for device in gpus:
            details[device.id] = {
                'name': device.name,
                'activity': device.activity * 100,  # Convert to percentage
                'memory_used': device.memory_used,
                'memory_total': device.memory_total,
                'temperature': device.temperature
            }
        return details

def main():
    print("Overall AMD GPU usage:")
    print(AMDGPU.get_gpu_usage())

    print("\nAMD GPU temperature:")
    print(AMDGPU.get_gpu_temperature())

    print("\nAMD GPU memory usage:")
    print(AMDGPU.get_gpu_memory_usage())

    print("\nNumber of AMD GPUs:")
    print(AMDGPU.get_gpu_count())

    print("\nAMD GPU details:")
    print(AMDGPU.get_gpu_details())

if __name__ == "__main__":
    main()

