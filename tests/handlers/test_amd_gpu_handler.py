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


# Utility function for assertions
def assert_result_or_message(result, expected_message, expected_data=None):
    """
    Assert the result is either an error message or matches expected data.
    """
    if isinstance(result, str):
        assert result == expected_message
    else:
        assert result == expected_data

# Parametrize GPU fixtures using their names
gpu_platforms = pytest.mark.parametrize(
    "gpu_fixture_name",
    ["no_gpus", "one_gpu", "multiple_gpus"],
)

# Test cases
@gpu_platforms
def test_get_gpu_count(mock_detect_gpus, gpu_fixture_name, request):
    """Test get_gpu_count for various GPU counts."""
    gpu_fixture = request.getfixturevalue(gpu_fixture_name)
    mock_detect_gpus(gpu_fixture)
    expected_count = {
        "no_gpus": 0,
        "one_gpu": 1,
        "multiple_gpus": 2,
    }[gpu_fixture_name]
    assert AMDGPU.get_gpu_count() == expected_count

@gpu_platforms
def test_get_gpu_usage(mock_detect_gpus, gpu_fixture_name, request):
    """Test get_gpu_usage for various scenarios."""
    gpu_fixture = request.getfixturevalue(gpu_fixture_name)
    mock_detect_gpus(gpu_fixture)
    expected_result = {
        "no_gpus": "No AMD GPUs found.",
        "one_gpu": {0: 50.0},
        "multiple_gpus": {0: 50.0, 1: 80.0},
    }[gpu_fixture_name]
    assert_result_or_message(AMDGPU.get_gpu_usage(), "No AMD GPUs found.", expected_result)

@gpu_platforms
def test_get_gpu_temperature(mock_detect_gpus, gpu_fixture_name, request):
    """Test get_gpu_temperature for various scenarios."""
    gpu_fixture = request.getfixturevalue(gpu_fixture_name)
    mock_detect_gpus(gpu_fixture)
    expected_result = {
        "no_gpus": "No AMD GPUs found.",
        "one_gpu": {0: 70},
        "multiple_gpus": {0: 70, 1: 65},
    }[gpu_fixture_name]
    assert_result_or_message(AMDGPU.get_gpu_temperature(), "No AMD GPUs found.", expected_result)

@gpu_platforms
def test_get_gpu_memory_usage(mock_detect_gpus, gpu_fixture_name, request):
    """Test get_gpu_memory_usage for various scenarios."""
    gpu_fixture = request.getfixturevalue(gpu_fixture_name)
    mock_detect_gpus(gpu_fixture)
    expected_result = {
        "no_gpus": "No AMD GPUs found.",
        "one_gpu": {0: {"used": 2000, "total": 4000}},
        "multiple_gpus": {
            0: {"used": 2000, "total": 4000},
            1: {"used": 3000, "total": 8000},
        },
    }[gpu_fixture_name]
    assert_result_or_message(
        AMDGPU.get_gpu_memory_usage(),
        "No AMD GPUs found.",
        expected_result,
    )


if __name__ == "__main__":
    pytest.main()
