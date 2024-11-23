import pytest
from unittest.mock import patch, MagicMock
from backend.gpu_handler import GPU  # Update the import based on your project structure


# Mocking GPUtil and subprocess
@pytest.fixture
def mock_gpus(monkeypatch):
    """Fixture to mock GPUtil.getGPUs."""
    mock_gpu = MagicMock()
    mock_gpu.id = 0
    mock_gpu.name = "NVIDIA GTX 1080"
    mock_gpu.load = 0.75  # 75% load
    mock_gpu.memoryTotal = 8192  # 8GB
    mock_gpu.memoryUsed = 4096  # 4GB
    mock_gpu.temperature = 65  # 65°C
    mock_gpu.uuid = "GPU-12345"
    monkeypatch.setattr("GPUtil.getGPUs", lambda: [mock_gpu])


@pytest.fixture
def mock_no_gpus(monkeypatch):
    """Fixture to mock GPUtil.getGPUs with no GPUs available."""
    monkeypatch.setattr("GPUtil.getGPUs", lambda: [])


@pytest.fixture
def mock_subprocess(monkeypatch):
    """Fixture to mock subprocess output for power usage."""
    def mock_check_output(cmd):
        if "nvidia-smi" in cmd:
            return b"75.5\n80.3\n"  # Mocked power usage in watts for two GPUs
        raise FileNotFoundError("nvidia-smi not found")

    monkeypatch.setattr("subprocess.check_output", mock_check_output)


# Test cases
def test_get_gpu_usage(mock_gpus):
    """Test GPU usage when GPUs are available."""
    result = GPU.get_gpu_usage()
    expected = {0: 75.0}
    assert result == expected


def test_get_gpu_usage_no_gpus(mock_no_gpus):
    """Test GPU usage when no GPUs are available."""
    result = GPU.get_gpu_usage()
    assert result == "No GPUs found."


def test_get_gpu_memory_usage(mock_gpus):
    """Test GPU memory usage when GPUs are available."""
    result = GPU.get_gpu_memory_usage()
    expected = {0: {'used': 4096, 'total': 8192}}
    assert result == expected


def test_get_gpu_memory_usage_no_gpus(mock_no_gpus):
    """Test GPU memory usage when no GPUs are available."""
    result = GPU.get_gpu_memory_usage()
    assert result == "No GPUs found."


def test_get_gpu_temperature(mock_gpus):
    """Test GPU temperature when GPUs are available."""
    result = GPU.get_gpu_temperature()
    expected = {0: 65}
    assert result == expected


def test_get_gpu_temperature_no_gpus(mock_no_gpus):
    """Test GPU temperature when no GPUs are available."""
    result = GPU.get_gpu_temperature()
    assert result == "No GPUs found."


def test_get_gpu_count(mock_gpus):
    """Test GPU count when GPUs are available."""
    result = GPU.get_gpu_count()
    assert result == 1


def test_get_gpu_count_no_gpus(mock_no_gpus):
    """Test GPU count when no GPUs are available."""
    result = GPU.get_gpu_count()
    assert result == 0


def test_get_gpu_details(mock_gpus):
    """Test GPU details when GPUs are available."""
    result = GPU.get_gpu_details()
    expected = {
        0: {
            'name': "NVIDIA GTX 1080",
            'load': 75.0,
            'memoryTotal': 8192,
            'memoryUsed': 4096,
            'temperature': 65,
            'uuid': "GPU-12345",
        }
    }
    assert result == expected


def test_get_gpu_details_no_gpus(mock_no_gpus):
    """Test GPU details when no GPUs are available."""
    result = GPU.get_gpu_details()
    assert result == "No GPUs found."


def test_get_gpu_power_usage(mock_subprocess):
    """Test GPU power usage when subprocess returns valid output."""
    result = GPU.get_gpu_power_usage()
    expected = {0: 75.5, 1: 80.3}
    assert result == expected


def test_get_gpu_power_usage_subprocess_failure(monkeypatch):
    """Test GPU power usage when subprocess fails."""
    def mock_check_output(cmd):
        raise FileNotFoundError("nvidia-smi not found")

    monkeypatch.setattr("subprocess.check_output", mock_check_output)
    result = GPU.get_gpu_power_usage()
    assert result == "nvidia-smi not found"


def test_get_gpu_power_usage_invalid_output(monkeypatch):
    """Test GPU power usage when subprocess returns invalid output."""
    def mock_check_output(cmd):
        return b"Invalid output"

    monkeypatch.setattr("subprocess.check_output", mock_check_output)
    result = GPU.get_gpu_power_usage()
    assert isinstance(result, str)
    assert "could not convert" in result


# Edge case: Multiple GPUs
@pytest.fixture
def mock_multiple_gpus(monkeypatch):
    """Fixture to mock multiple GPUs."""
    gpu1 = MagicMock()
    gpu1.id = 0
    gpu1.name = "NVIDIA GTX 1080"
    gpu1.load = 0.75
    gpu1.memoryTotal = 8192
    gpu1.memoryUsed = 4096
    gpu1.temperature = 65
    gpu1.uuid = "GPU-12345"

    gpu2 = MagicMock()
    gpu2.id = 1
    gpu2.name = "NVIDIA RTX 3090"
    gpu2.load = 0.50
    gpu2.memoryTotal = 24576
    gpu2.memoryUsed = 12288
    gpu2.temperature = 70
    gpu2.uuid = "GPU-67890"

    monkeypatch.setattr("GPUtil.getGPUs", lambda: [gpu1, gpu2])


def test_get_gpu_details_multiple_gpus(mock_multiple_gpus):
    """Test GPU details for multiple GPUs."""
    result = GPU.get_gpu_details()
    expected = {
        0: {
            'name': "NVIDIA GTX 1080",
            'load': 75.0,
            'memoryTotal': 8192,
            'memoryUsed': 4096,
            'temperature': 65,
            'uuid': "GPU-12345",
        },
        1: {
            'name': "NVIDIA RTX 3090",
            'load': 50.0,
            'memoryTotal': 24576,
            'memoryUsed': 12288,
            'temperature': 70,
            'uuid': "GPU-67890",
        }
    }
    assert result == expected


if __name__ == "__main__":
    pytest.main()
