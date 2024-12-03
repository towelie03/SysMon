import subprocess  # Add this import at the beginning of your test file
import pytest
from backend.gpu_handler import (
    GPU,
)  # Adjust the import based on your directory structure


# Mock GPU Data
class MockGPU:
    def __init__(self, id, load, memoryUsed, memoryTotal, temperature, name, uuid):
        self.id = id
        self.load = load
        self.memoryUsed = memoryUsed
        self.memoryTotal = memoryTotal
        self.temperature = temperature
        self.name = name
        self.uuid = uuid


@pytest.fixture
def mock_gpus(monkeypatch):
    """Fixture to mock GPUtil.getGPUs."""
    mock_gpu_list = [
        MockGPU(0, 0.75, 2048, 8192, 70, "NVIDIA GeForce GTX 1080", "uuid-123"),
        MockGPU(1, 0.50, 1024, 4096, 60, "NVIDIA GeForce GTX 1070", "uuid-456"),
    ]
    monkeypatch.setattr("GPUtil.getGPUs", lambda: mock_gpu_list)


@pytest.fixture
def mock_no_gpus(monkeypatch):
    """Fixture to simulate no GPUs found."""
    monkeypatch.setattr("GPUtil.getGPUs", lambda: [])


@pytest.fixture
def mock_subprocess_success(monkeypatch):
    """Fixture to mock successful subprocess call to nvidia-smi."""
    mock_output = "150.0\n120.5\n"
    monkeypatch.setattr(
        "subprocess.check_output", lambda cmd: mock_output.encode("utf-8")
    )


@pytest.fixture
def mock_subprocess_failure(monkeypatch):
    """Fixture to mock a failure in subprocess call."""

    def _raise_exception(*args, **kwargs):
        raise subprocess.SubprocessError("nvidia-smi not found")

    monkeypatch.setattr("subprocess.check_output", _raise_exception)


# Test cases
def test_get_gpu_usage(mock_gpus):
    """Test GPU usage with multiple GPUs."""
    result = GPU.get_gpu_usage()
    expected = {0: 75.0, 1: 50.0}
    assert result == expected


def test_get_gpu_usage_no_gpus(mock_no_gpus):
    """Test GPU usage when no GPUs are found."""
    result = GPU.get_gpu_usage()
    assert result == "No GPUs found."


def test_get_gpu_memory_usage(mock_gpus):
    """Test GPU memory usage."""
    result = GPU.get_gpu_memory_usage()
    expected = {
        0: {"used": 2048, "total": 8192},
        1: {"used": 1024, "total": 4096},
    }
    assert result == expected


def test_get_gpu_memory_usage_no_gpus(mock_no_gpus):
    """Test GPU memory usage when no GPUs are found."""
    result = GPU.get_gpu_memory_usage()
    assert result == "No GPUs found."


def test_get_gpu_temperature(mock_gpus):
    """Test GPU temperature."""
    result = GPU.get_gpu_temperature()
    expected = {0: 70, 1: 60}
    assert result == expected


def test_get_gpu_temperature_no_gpus(mock_no_gpus):
    """Test GPU temperature when no GPUs are found."""
    result = GPU.get_gpu_temperature()
    assert result == "No GPUs found."


def test_get_gpu_count(mock_gpus):
    """Test GPU count."""
    result = GPU.get_gpu_count()
    assert result == 2


def test_get_gpu_count_no_gpus(mock_no_gpus):
    """Test GPU count when no GPUs are found."""
    result = GPU.get_gpu_count()
    assert result == 0


def test_get_gpu_details(mock_gpus):
    """Test GPU details."""
    result = GPU.get_gpu_details()
    expected = {
        0: {
            "name": "NVIDIA GeForce GTX 1080",
            "load": 75.0,
            "memoryTotal": 8192,
            "memoryUsed": 2048,
            "temperature": 70,
            "uuid": "uuid-123",
        },
        1: {
            "name": "NVIDIA GeForce GTX 1070",
            "load": 50.0,
            "memoryTotal": 4096,
            "memoryUsed": 1024,
            "temperature": 60,
            "uuid": "uuid-456",
        },
    }
    assert result == expected


def test_get_gpu_details_no_gpus(mock_no_gpus):
    """Test GPU details when no GPUs are found."""
    result = GPU.get_gpu_details()
    assert result == "No GPUs found."


def test_get_gpu_power_usage(mock_subprocess_success):
    """Test GPU power usage with subprocess success."""
    result = GPU.get_gpu_power_usage()
    expected = {0: 150.0, 1: 120.5}
    assert result == expected


def test_get_gpu_power_usage_failure(mock_subprocess_failure):
    """Test GPU power usage when subprocess fails."""
    result = GPU.get_gpu_power_usage()
    assert result == "nvidia-smi not found"


def test_get_gpu_power_usage_invalid_output(monkeypatch):
    """Test GPU power usage with invalid subprocess output."""
    monkeypatch.setattr("subprocess.check_output", lambda cmd: b"invalid\noutput\n")
    result = GPU.get_gpu_power_usage()
    assert isinstance(result, str)
    assert "could not convert string to float" in result


# Edge Case: GPUs with no load
def test_get_gpu_usage_no_load(monkeypatch):
    """Test GPU usage when GPUs have zero load."""
    mock_gpu_list = [
        MockGPU(0, 0.0, 2048, 8192, 70, "NVIDIA GeForce GTX 1080", "uuid-123"),
    ]
    monkeypatch.setattr("GPUtil.getGPUs", lambda: mock_gpu_list)
    result = GPU.get_gpu_usage()
    expected = {0: 0.0}
    assert result == expected


if __name__ == "__main__":
    pytest.main()
