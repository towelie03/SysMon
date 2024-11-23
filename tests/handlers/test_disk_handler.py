import pytest
import psutil
from backend.disk_handler import Disk

# Fixtures for mocking
@pytest.fixture
def mock_disk_partitions(monkeypatch):
    """Fixture to mock psutil.disk_partitions."""
    def _mock():
        return [
            psutil._common.sdiskpart(device='/dev/sda1', mountpoint='/', fstype='ext4', opts='rw'),
            psutil._common.sdiskpart(device='/dev/sdb1', mountpoint='/data', fstype='xfs', opts='rw'),
        ]
    monkeypatch.setattr(psutil, "disk_partitions", _mock)


@pytest.fixture
def mock_disk_usage(monkeypatch):
    """Fixture to mock psutil.disk_usage."""
    def _mock(path):
        if path == '/':
            return psutil._common.sdiskusage(total=500000000000, used=200000000000, free=300000000000, percent=40.0)
        raise FileNotFoundError("Invalid path")
    monkeypatch.setattr(psutil, "disk_usage", _mock)


@pytest.fixture
def mock_disk_io_counters(monkeypatch):
    """Fixture to mock psutil.disk_io_counters."""
    def _mock(perdisk=False):
        if perdisk:
            return {
                'sda': psutil._common.sdiskio(read_count=1000, write_count=500, read_bytes=2048, write_bytes=4096,
                                              read_time=10, write_time=5),
                'sdb': psutil._common.sdiskio(read_count=500, write_count=1000, read_bytes=1024, write_bytes=2048,
                                              read_time=15, write_time=20),
            }
        return psutil._common.sdiskio(read_count=1500, write_count=1500, read_bytes=3072, write_bytes=6144,
                                      read_time=25, write_time=25)
    monkeypatch.setattr(psutil, "disk_io_counters", _mock)


@pytest.fixture
def mock_sleep(monkeypatch):
    """Fixture to mock time.sleep."""
    monkeypatch.setattr("time.sleep", lambda x: None)


@pytest.fixture
def mock_time(monkeypatch):
    """Fixture to mock time.time."""
    initial_time = [1000]  # Mutable object to allow updates

    def _mock():
        current = initial_time[0]
        initial_time[0] += 1  # Increment for each call
        return current
    monkeypatch.setattr("time.time", _mock)


# Test cases
def test_get_disk_partitions(mock_disk_partitions):
    """Test get_disk_partitions."""
    result = Disk.get_disk_partitions()
    expected = [
        {'device': '/dev/sda1', 'mountpoint': '/', 'fstype': 'ext4', 'opts': 'rw'},
        {'device': '/dev/sdb1', 'mountpoint': '/data', 'fstype': 'xfs', 'opts': 'rw'},
    ]
    assert result == expected


def test_get_disk_usage(mock_disk_usage):
    """Test get_disk_usage."""
    result = Disk.get_disk_usage('/')
    expected = {'total': 500000000000, 'used': 200000000000, 'free': 300000000000, 'percent': 40.0}
    assert result == expected


def test_get_disk_usage_invalid_path(mock_disk_usage):
    """Test get_disk_usage with invalid path."""
    with pytest.raises(FileNotFoundError):
        Disk.get_disk_usage('/invalid')


def test_get_disk_io_counters(mock_disk_io_counters):
    """Test get_disk_io_counters."""
    result = Disk.get_disk_io_counters()
    expected = {
        'read_count': 1500,
        'write_count': 1500,
        'read_bytes': 3072,
        'write_bytes': 6144,
        'read_time': 25,
        'write_time': 25,
    }
    assert result == expected


def test_get_disk_io_counters_per_disk(mock_disk_io_counters):
    """Test get_disk_io_counters_per_disk."""
    result = Disk.get_disk_io_counters_per_disk()
    expected = {
        'sda': {'read_count': 1000, 'write_count': 500, 'read_bytes': 2048, 'write_bytes': 4096, 'read_time': 10, 'write_time': 5},
        'sdb': {'read_count': 500, 'write_count': 1000, 'read_bytes': 1024, 'write_bytes': 2048, 'read_time': 15, 'write_time': 20},
    }
    assert result == expected


@pytest.fixture
def mock_disk_io_counters_for_active_time(monkeypatch):
    """Fixture to mock psutil.disk_io_counters for active time percentage."""
    counters = [
        psutil._common.sdiskio(read_count=1000, write_count=500, read_bytes=2048, write_bytes=4096,
                               read_time=10, write_time=5),  # Initial counters
        psutil._common.sdiskio(read_count=1000, write_count=500, read_bytes=2048, write_bytes=4096,
                               read_time=25, write_time=25),  # Updated counters
    ]
    call_count = [0]  # Mutable object to track calls

    def _mock(perdisk=False):
        if call_count[0] < len(counters):
            result = counters[call_count[0]]
            call_count[0] += 1
            return result
        return counters[-1]  # Return the last set of counters if called more times

    monkeypatch.setattr(psutil, "disk_io_counters", _mock)


def test_get_disk_active_time_percentage(mock_disk_io_counters_for_active_time, mock_sleep, mock_time):
    """Test get_disk_active_time_percentage."""
    result = Disk.get_disk_active_time_percentage(interval=1)
    # Active time = (25 - 10) ms read_time + (25 - 5) ms write_time = 35 ms
    # Interval duration = 1 second = 1000 ms
    expected = (35 / 1000) * 100  # 3.5%
    assert result == round(expected, 2)


if __name__ == "__main__":
    pytest.main()