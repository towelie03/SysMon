import pytest
from backend.amd_gpu_handler import AMDGPU


# Mocked GPU device
class MockGPU:
    def __init__(self, id, name, activity, temperature, memory_used, memory_total):
        self.id = id
        self.name = name
        self.activity = activity  # Fraction [0.0 - 1.0]
        self.temperature = temperature
        self.memory_used = memory_used
        self.memory_total = memory_total


# Fixtures for test data
@pytest.fixture
def no_gpus():
    """Fixture for no detected GPUs."""
    return None


@pytest.fixture
def one_gpu():
    """Fixture for one detected GPU."""
    return [MockGPU(0, "AMD RX 580", 0.5, 70, 2000, 4000)]


@pytest.fixture
def multiple_gpus():
    """Fixture for multiple detected GPUs."""
    return [
        MockGPU(0, "AMD RX 580", 0.5, 70, 2000, 4000),
        MockGPU(1, "AMD RX 5700", 0.8, 65, 3000, 8000),
    ]


@pytest.fixture
def mock_detect_gpus(monkeypatch):
    """Fixture to mock GPU detection."""
    def _mock(gpu_list):
        monkeypatch.setattr("pyamdgpuinfo.detect_gpus", lambda: gpu_list)
    return _mock


# Test cases
def test_check_gpus_no_devices(mock_detect_gpus, no_gpus):
    """Test _check_gpus when no devices are found."""
    mock_detect_gpus(no_gpus)
    devices = AMDGPU._check_gpus()
    assert devices is None


def test_check_gpus_with_devices(mock_detect_gpus, one_gpu):
    """Test _check_gpus with detected devices."""
    mock_detect_gpus(one_gpu)
    devices = AMDGPU._check_gpus()
    assert devices == one_gpu


def test_get_gpu_usage_no_gpus(mock_detect_gpus, no_gpus):
    """Test get_gpu_usage when no GPUs are detected."""
    mock_detect_gpus(no_gpus)
    result = AMDGPU.get_gpu_usage()
    assert result == "No AMD GPUs found."


def test_get_gpu_usage_with_gpus(mock_detect_gpus, multiple_gpus):
    """Test get_gpu_usage with detected GPUs."""
    mock_detect_gpus(multiple_gpus)
    result = AMDGPU.get_gpu_usage()
    expected = {0: 50.0, 1: 80.0}  # Activity as a percentage
    assert result == expected


def test_get_gpu_usage_with_zero_activity(mock_detect_gpus):
    """Test get_gpu_usage with GPUs that have 0 activity."""
    mock_devices = [
        MockGPU(0, "AMD RX 580", 0.0, 70, 2000, 4000),  # 0 activity
        MockGPU(1, "AMD RX 5700", 0.0, 65, 3000, 8000),  # 0 activity
    ]
    mock_detect_gpus(mock_devices)
    result = AMDGPU.get_gpu_usage()
    expected = {0: 0.0, 1: 0.0}  # 0% activity
    assert result == expected


def test_get_gpu_temperature_no_gpus(mock_detect_gpus, no_gpus):
    """Test get_gpu_temperature when no GPUs are detected."""
    mock_detect_gpus(no_gpus)
    result = AMDGPU.get_gpu_temperature()
    assert result == "No AMD GPUs found."


def test_get_gpu_temperature_with_gpus(mock_detect_gpus, multiple_gpus):
    """Test get_gpu_temperature with detected GPUs."""
    mock_detect_gpus(multiple_gpus)
    result = AMDGPU.get_gpu_temperature()
    expected = {0: 70, 1: 65}  # Temperatures in degrees
    assert result == expected


def test_get_gpu_temperature_extreme_values(mock_detect_gpus):
    """Test get_gpu_temperature with extreme temperature values."""
    mock_devices = [
        MockGPU(0, "AMD RX 580", 0.5, -10, 2000, 4000),  # Below 0°C
        MockGPU(1, "AMD RX 5700", 0.8, 120, 3000, 8000),  # Above 100°C
    ]
    mock_detect_gpus(mock_devices)
    result = AMDGPU.get_gpu_temperature()
    expected = {0: -10, 1: 120}
    assert result == expected


def test_get_gpu_memory_usage_no_gpus(mock_detect_gpus, no_gpus):
    """Test get_gpu_memory_usage when no GPUs are detected."""
    mock_detect_gpus(no_gpus)
    result = AMDGPU.get_gpu_memory_usage()
    assert result == "No AMD GPUs found."


def test_get_gpu_memory_usage_with_gpus(mock_detect_gpus, multiple_gpus):
    """Test get_gpu_memory_usage with detected GPUs."""
    mock_detect_gpus(multiple_gpus)
    result = AMDGPU.get_gpu_memory_usage()
    expected = {
        0: {"used": 2000, "total": 4000},
        1: {"used": 3000, "total": 8000},
    }
    assert result == expected


def test_get_gpu_memory_usage_invalid_memory(mock_detect_gpus):
    """Test get_gpu_memory_usage with invalid memory values."""
    mock_devices = [
        MockGPU(0, "AMD RX 580", 0.5, 70, -100, 4000),  # Negative used memory
        MockGPU(1, "AMD RX 5700", 0.8, 65, 0, 8000),    # Zero used memory
    ]
    mock_detect_gpus(mock_devices)
    result = AMDGPU.get_gpu_memory_usage()
    expected = {
        0: {"used": -100, "total": 4000},
        1: {"used": 0, "total": 8000},
    }
    assert result == expected


def test_get_gpu_count_no_gpus(mock_detect_gpus, no_gpus):
    """Test get_gpu_count when no GPUs are detected."""
    mock_detect_gpus(no_gpus)
    result = AMDGPU.get_gpu_count()
    assert result == 0


def test_get_gpu_count_with_gpus(mock_detect_gpus, multiple_gpus):
    """Test get_gpu_count with detected GPUs."""
    mock_detect_gpus(multiple_gpus)
    result = AMDGPU.get_gpu_count()
    assert result == 2


def test_get_gpu_count_max_gpus(mock_detect_gpus):
    """Test get_gpu_count for the maximum number of GPUs."""
    mock_devices = [MockGPU(i, f"AMD GPU {i}", 0.5, 50 + i, 2000, 4000) for i in range(100)]
    mock_detect_gpus(mock_devices)
    result = AMDGPU.get_gpu_count()
    assert result == 100


def test_get_gpu_details_no_gpus(mock_detect_gpus, no_gpus):
    """Test get_gpu_details when no GPUs are detected."""
    mock_detect_gpus(no_gpus)
    result = AMDGPU.get_gpu_details()
    assert result == "No AMD GPUs found."


def test_get_gpu_details_with_gpus(mock_detect_gpus, multiple_gpus):
    """Test get_gpu_details with detected GPUs."""
    mock_detect_gpus(multiple_gpus)
    result = AMDGPU.get_gpu_details()
    expected = {
        0: {
            "name": "AMD RX 580",
            "activity": 50.0,
            "memory_used": 2000,
            "memory_total": 4000,
            "temperature": 70,
        },
        1: {
            "name": "AMD RX 5700",
            "activity": 80.0,
            "memory_used": 3000,
            "memory_total": 8000,
            "temperature": 65,
        },
    }
    assert result == expected


def test_get_gpu_details_missing_attributes(mock_detect_gpus):
    """Test get_gpu_details with GPUs missing some attributes."""
    mock_devices = [
        MockGPU(0, "AMD RX 580", 0.5, None, 2000, 4000),  # Missing temperature
        MockGPU(1, "AMD RX 5700", 0.8, 65, None, None),   # Missing memory
    ]
    mock_detect_gpus(mock_devices)
    result = AMDGPU.get_gpu_details()
    expected = {
        0: {
            "name": "AMD RX 580",
            "activity": 50.0,
            "memory_used": 2000,
            "memory_total": 4000,
            "temperature": None,
        },
        1: {
            "name": "AMD RX 5700",
            "activity": 80.0,
            "memory_used": None,
            "memory_total": None,
            "temperature": 65,
        },
    }
    assert result == expected


def test_single_gpu_minimal_resources(mock_detect_gpus):
    """Test get_gpu_details for a single GPU with minimal resources."""
    mock_devices = [MockGPU(0, "AMD Test", 0.1, 1, 1, 1)]  # Minimal values
    mock_detect_gpus(mock_devices)
    result = AMDGPU.get_gpu_details()
    expected = {
        0: {
            "name": "AMD Test",
            "activity": 10.0,  # 10% activity
            "memory_used": 1,
            "memory_total": 1,
            "temperature": 1,
        }
    }
    assert result == expected
