import psutil

class Memory:
    
    @staticmethod
    def get_virtual_memory():
        """
        Returns information about virtual memory usage.
        """
        mem = psutil.virtual_memory()
        return {
            'total': mem.total,
            'available': mem.available,
            'used': mem.used,
            'free': mem.free,
            'percent': mem.percent
        }
    
    @staticmethod
    def get_swap_memory():
        """
        Returns information about swap memory usage.
        """
        swap = psutil.swap_memory()
        return {
            'total': swap.total,
            'used': swap.used,
            'free': swap.free,
            'percent': swap.percent,
            'sin': swap.sin,
            'sout': swap.sout
        }
    
    @staticmethod
    def get_memory_percent():
        """
        Returns the percentage of memory being used.
        """
        return psutil.virtual_memory().percent

    @staticmethod
    def get_memory_usage():
        """
        Returns the current memory usage in bytes.
        """
        return psutil.virtual_memory().used

    @staticmethod
    def get_memory_available():
        """
        Returns the amount of memory available for use.
        """
        return psutil.virtual_memory().available

    @staticmethod
    def get_memory_total():
        """
        Returns the total amount of memory.
        """
        return psutil.virtual_memory().total

def main():
    print("Virtual Memory:")
    print(Memory.get_virtual_memory())

    print("\nSwap Memory:")
    print(Memory.get_swap_memory())

    print("\nMemory Usage Percentage:")
    print(f"{Memory.get_memory_percent()}%")

    print("\nMemory Used:")
    print(f"{Memory.get_memory_usage()} bytes")

    print("\nMemory Available:")
    print(f"{Memory.get_memory_available()} bytes")

    print("\nTotal Memory:")
    print(f"{Memory.get_memory_total()} bytes")

if __name__ == "__main__":
    main()
