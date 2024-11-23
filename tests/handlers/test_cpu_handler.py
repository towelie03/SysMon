import pytest
import psutil
import os
import io
from collections import namedtuple
from backend.cpu_handler import CPU

# Fixtures for mocking
@pytest.fixture
def mock_cpu_percent(monkeypatch):
    """Fixture to mock psutil.cpu_percent."""
    def _mock(interval=1, percpu=False):
        if percpu:
            return [10.0, 15.0, 20.0]  # Mock per-core usage
        return 25.0  # Mock overall usage
    monkeypatch.setattr(psutil, "cpu_percent", _mock)

@pytest.fixture
def mock_cpu_freq(monkeypatch):
    """Fixture to mock psutil.cpu_freq."""
    def _mock():
        return psutil._common.scpufreq(2400.0, 800.0, 3600.0)  # Positional arguments
    monkeypatch.setattr(psutil, "cpu_freq", _mock)

@pytest.fixture
def mock_cpu_count(monkeypatch):
    """Fixture to mock psutil.cpu_count."""
    def _mock(logical=True):
        return 8 if logical else 4
    monkeypatch.setattr(psutil, "cpu_count", _mock)

@pytest.fixture
def mock_getloadavg(monkeypatch):
    """Fixture to mock os.getloadavg."""
    def _mock():
        return (0.5, 1.0, 1.5)
    monkeypatch.setattr(os, "getloadavg", _mock)

@pytest.fixture
def mock_cpu_temperature(monkeypatch):
    """Fixture to mock CPU temperature reading."""
    def mock_isfile(path):
        return path == "/sys/class/thermal/thermal_zone0/temp"

    def mock_open(path, *args, **kwargs):
        if path == "/sys/class/thermal/thermal_zone0/temp":
            return io.StringIO("45000")  # Mock temperature as 45.0°C
        else:
            raise FileNotFoundError

    monkeypatch.setattr(os.path, "isfile", mock_isfile)
    monkeypatch.setattr("builtins.open", mock_open)

@pytest.fixture
def mock_cpu_times(monkeypatch):
    """Fixture to mock psutil.cpu_times."""
    def _mock():
        # Explicitly define the expected fields for the namedtuple
        CpuTimes = namedtuple(
            "CpuTimes",
            [
                "user", "nice", "system", "idle", "iowait",
                "irq", "softirq", "steal", "guest", "guest_nice"
            ]
        )
        return CpuTimes(
            user=1234.0,
            nice=10.0,
            system=234.0,
            idle=5678.0,
            iowait=50.0,
            irq=5.0,
            softirq=2.0,
            steal=1.0,
            guest=0.0,
            guest_nice=0.0
        )
    monkeypatch.setattr(psutil, "cpu_times", _mock)

@pytest.fixture
def mock_uptime(monkeypatch):
    """Fixture to mock uptime.uptime."""
    def _mock():
        return 3600.0  # Mock uptime of 1 hour
    monkeypatch.setattr("uptime.uptime", _mock)

# Test cases
def test_get_cpu_usage(mock_cpu_percent):
    """Test get_cpu_usage."""
    result = CPU.get_cpu_usage()
    assert result == 25.0

def test_get_per_cpu_usage(mock_cpu_percent):
    """Test get_per_cpu_usage."""
    result = CPU.get_per_cpu_usage()
    assert result == [10.0, 15.0, 20.0]

def test_get_cpu_frequency(mock_cpu_freq):
    """Test get_cpu_frequency."""
    result = CPU.get_cpu_frequency()
    expected = {"current": 2400.0, "min": 800.0, "max": 3600.0}
    assert result == expected

def test_get_cpu_count(mock_cpu_count):
    """Test get_cpu_count."""
    logical_count = CPU.get_cpu_count(logical=True)
    physical_count = CPU.get_cpu_count(logical=False)
    assert logical_count == 8
    assert physical_count == 4

def test_get_load_average(mock_getloadavg):
    """Test get_load_average."""
    result = CPU.get_load_average()
    assert result == (0.5, 1.0, 1.5)

def test_get_cpu_temperature(mock_cpu_temperature):
    """Test get_cpu_temperature."""
    result = CPU.get_cpu_temperature()
    assert result == 45.0

def test_get_cpu_times(mock_cpu_times):
    """Test get_cpu_times."""
    result = CPU.get_cpu_times()
    expected = {
        "user": 1234.0,
        "nice": 10.0,
        "system": 234.0,
        "idle": 5678.0,
        "iowait": 50.0,
        "irq": 5.0,
        "softirq": 2.0,
        "steal": 1.0,
        "guest": 0.0,
        "guest_nice": 0.0
    }
    assert result == expected

def test_get_uptime(mock_uptime):
    """Test get_uptime."""
    result = CPU.get_uptime()
    assert result == 3600.0
