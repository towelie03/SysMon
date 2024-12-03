import requests

BASE_URL = "http://127.0.0.1:8000"


def fetch_cpu_usage():
    try:
        response = requests.get(f"{BASE_URL}/cpu/usage")
        response.raise_for_status()
        return response.json()["cpu_usage"]
    except Exception as e:
        print(f"Error fetching CPU usage: {e}")
        return None


def fetch_memory_percent():
    try:
        response = requests.get(f"{BASE_URL}/memory/percent")
        response.raise_for_status()
        return response.json()["memory_percent"]
    except Exception as e:
        print(f"Error fetching memory percent: {e}")
        return None


def fetch_network_bandwidth():
    try:
        response = requests.get(f"{BASE_URL}/network/bandwidth")
        response.raise_for_status()
        return response.json()["bandwidth_usage"]
    except Exception as e:
        print(f"Error fetching network bandwidth: {e}")
        return None
