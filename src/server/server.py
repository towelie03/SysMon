from fastapi import FastAPI, HTTPException
from proccess_handler import Process
from cpu_handler import CPU
from mem_handler import Memory
from network_handler import Network
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS configuration
origins = ["*"]  # Allow all origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

@app.get("/processes", response_model=list)
def get_all_processes():
    """
    Endpoint to get all running processes.
    """
    processes = Process.list_all_processes()
    return processes

@app.get("/processes/{pid}", response_model=dict)
def get_process_by_pid(pid: int):
    """
    Endpoint to get a process by its PID.
    """
    process = Process.get_process_info(pid)
    if process:
        return process
    else:
        raise HTTPException(status_code=404, detail=f"Process with PID {pid} not found")
    
@app.post("/killprocess/{pid}")
def post_kill_process(pid:int):
    result_string= Process.kill_process(pid)
    res = {
        "res" : result_string
    }
    return res

#CPU
@app.get("/cpu/all")
def get_all_cpu_data():
    cpu_data = {
        "cpu_usage": CPU.get_cpu_usage(),
        "per_cpu_usage": CPU.get_per_cpu_usage(),
        "cpu_frequency": CPU.get_cpu_frequency(),
        "cpu_count": CPU.get_cpu_count(),
        "load_average": CPU.get_load_average(),
        "core_utilization": CPU.get_core_utilization(),
        "cpu_temperature": CPU.get_cpu_temperature(),
        "cpu_times": CPU.get_cpu_times()
    }
    return cpu_data

@app.get("/cpu/usage")
def cpu_usage():
    return {"cpu_usage": CPU.get_cpu_usage()}

@app.get("/cpu/per_cpu_usage")
def per_cpu_usage():
    return {"per_cpu_usage": CPU.get_per_cpu_usage()}

@app.get("/cpu/frequency")
def cpu_frequency():
    return {"cpu_frequency": CPU.get_cpu_frequency()}

@app.get("/cpu/count")
def cpu_count():
    return {"cpu_count": CPU.get_cpu_count()}

@app.get("/cpu/load_average")
def load_average():
    return {"load_average": CPU.get_load_average()}

@app.get("/cpu/core_utilization")
def core_utilization():
    return {"core_utilization": CPU.get_core_utilization()}

@app.get("/cpu/temperature")
def cpu_temperature():
    return {"cpu_temperature": CPU.get_cpu_temperature()}

@app.get("/cpu/times")
def cpu_times():
    return {"cpu_times": CPU.get_cpu_times()}

#MEMORY
@app.get("/memory/all")
def get_all_memory_data():
    memory_data = {
        "virtual_memory": Memory.get_virtual_memory(),
        "swap_memory": Memory.get_swap_memory(),
        "memory_percent": Memory.get_memory_percent(),
        "memory_usage": Memory.get_memory_usage(),
        "memory_available": Memory.get_memory_available(),
        "memory_total": Memory.get_memory_total()
    }
    return memory_data

@app.get("/memory/virtual")
def virtual_memory():
    return {"virtual_memory": Memory.get_virtual_memory()}

@app.get("/memory/swap")
def swap_memory():
    return {"swap_memory": Memory.get_swap_memory()}

@app.get("/memory/percent")
def memory_percent():
    return {"memory_percent": Memory.get_memory_percent()}

@app.get("/memory/usage")
def memory_usage():
    return {"memory_usage": Memory.get_memory_usage()}

@app.get("/memory/available")
def memory_available():
    return {"memory_available": Memory.get_memory_available()}

@app.get("/memory/total")
def memory_total():
    return {"memory_total": Memory.get_memory_total()}

#NETWORK HANDLER
@app.get("/network/bandwidth")
def get_bandwidth_usage():
    return {"bandwidth_usage": Network.get_bandwidth_usage()}
