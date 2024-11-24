from pydantic import BaseModel

class UserSettings(BaseModel):
    cpu_threshold: int = 80
    memory_threshold: int = 80
    disk_threshold: int = 80
    network_threshold: int = 1000000
    gpu_threshold: int = 80
    check_interval: int = 10
    theme: str = "catpuccin"