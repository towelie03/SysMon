# cpu_stress.py
import multiprocessing

def cpu_intensive_task():
    while True:
        pass  # Keeps CPU busy

# Run multiple processes to simulate high CPU usage
if __name__ == "__main__":
    processes = []
    for _ in range(multiprocessing.cpu_count()):  # Use all available cores
        process = multiprocessing.Process(target=cpu_intensive_task)
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
