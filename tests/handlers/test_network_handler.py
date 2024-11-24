import pytest
import psutil
import socket
from backend.network_handler import Network


# Fixtures for mocking
@pytest.fixture
def mock_net_io_counters(monkeypatch):
    """Fixture to mock psutil.net_io_counters."""
    class MockNetIoCounters:
        bytes_sent = 100000000  # 100 MB
        bytes_recv = 150000000  # 150 MB
        packets_sent = 500000
        packets_recv = 750000

    monkeypatch.setattr(psutil, "net_io_counters", lambda: MockNetIoCounters())


@pytest.fixture
def mock_time(monkeypatch):
    """Fixture to mock time.sleep and time.time."""
    monkeypatch.setattr("time.sleep", lambda x: None)
    mock_time = iter([1000, 1001])  # Simulate time increments
    monkeypatch.setattr("time.time", lambda: next(mock_time))


@pytest.fixture
def mock_socket_gethostname(monkeypatch):
    """Fixture to mock socket.gethostname."""
    monkeypatch.setattr(socket, "gethostname", lambda: "mocked-hostname")


@pytest.fixture
def mock_socket_gethostbyname(monkeypatch):
    """Fixture to mock socket.gethostbyname."""
    monkeypatch.setattr(socket, "gethostbyname", lambda x: "192.168.1.1")


@pytest.fixture
def mock_socket_getaddrinfo(monkeypatch):
    """Fixture to mock socket.getaddrinfo for IPv6."""
    def _mock(hostname, *args, **kwargs):
        return [(socket.AF_INET6, None, None, None, ("fe80::1", 0, 0, 0))]
    monkeypatch.setattr(socket, "getaddrinfo", _mock)


@pytest.fixture
def mock_net_if_addrs(monkeypatch):
    """Fixture to mock psutil.net_if_addrs."""
    def _mock():
        return {
            "wlan0": [],
            "eth0": [],
        }
    monkeypatch.setattr(psutil, "net_if_addrs", _mock)


@pytest.fixture
def mock_net_if_stats(monkeypatch):
    """Fixture to mock psutil.net_if_stats."""
    class MockInterfaceStats:
        isup = True

    def _mock():
        return {
            "wlan0": MockInterfaceStats(),
            "eth0": MockInterfaceStats(),
        }
    monkeypatch.setattr(psutil, "net_if_stats", _mock)


# Test cases
def test_get_bandwidth_usage(mock_net_io_counters):
    """Test get_bandwidth_usage."""
    result = Network.get_bandwidth_usage()
    expected = {
        "bytes_sent": 100000000,
        "bytes_received": 150000000,
        "packets_sent": 500000,
        "packets_received": 750000,
    }
    assert result == expected


def test_bytes_convert():
    """Test bytes_convert for various cases."""
    assert Network.bytes_convert(1024) == "1.00 KB/s"
    assert Network.bytes_convert(1048576) == "1.00 MB/s"
    assert Network.bytes_convert(1073741824) == "1.00 GB/s"
    assert Network.bytes_convert(512) == "512.00 B/s"


def test_monitor_total_traffic(mock_net_io_counters, mock_time):
    """Test monitor_total_traffic."""
    result = Network.monitor_total_traffic(interval=1)
    expected = {
        "sent": 0.0,  # No change in counters between intervals
        "recv": 0.0,
    }
    assert result == expected


def test_get_primary_ipv4(mock_socket_gethostname, mock_socket_gethostbyname):
    """Test get_primary_ipv4."""
    result = Network.get_primary_ipv4()
    assert result == "192.168.1.1"


def test_get_primary_ipv6(mock_socket_gethostname, mock_socket_getaddrinfo):
    """Test get_primary_ipv6."""
    result = Network.get_primary_ipv6()
    assert result == "fe80::1"


def test_get_primary_ipv6_no_ipv6(monkeypatch):
    """Test get_primary_ipv6 when no IPv6 is available."""
    monkeypatch.setattr(socket, "getaddrinfo", lambda *args, **kwargs: [])
    result = Network.get_primary_ipv6()
    assert result is None


def test_get_primary_connection_type_wifi(mock_net_if_addrs, mock_net_if_stats):
    """Test get_primary_connection_type for WiFi."""
    result = Network.get_primary_connection_type()
    assert result == "WiFi"


def test_get_primary_connection_type_ethernet(mock_net_if_addrs, mock_net_if_stats, monkeypatch):
    """Test get_primary_connection_type for Ethernet."""
    # Set the `isup` attribute of `wlan0` to False to simulate Ethernet connection.
    def mock_net_if_stats_override():
        class MockInterfaceStats:
            def __init__(self, isup):
                self.isup = isup

        return {
            "wlan0": MockInterfaceStats(isup=False),
            "eth0": MockInterfaceStats(isup=True),
        }

    monkeypatch.setattr(psutil, "net_if_stats", mock_net_if_stats_override)
    result = Network.get_primary_connection_type()
    assert result == "Ethernet"



if __name__ == "__main__":
    pytest.main()
