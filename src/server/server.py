from fastapi import FastAPI, HTTPException
from proccess_handler import Process

app = FastAPI()

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
    process = Process.get_process_by_pid(pid)
    if process:
        return process
    else:
        raise HTTPException(status_code=404, detail=f"Process with PID {pid} not found")
