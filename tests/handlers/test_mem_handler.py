import pytest
import psutil
from backend.mem_handler import Memory

# Fixtures for mocking psutil functions
@pytest.fixture
def mock_virtual_memory(monkeypatch):
    """Fixture to mock psutil.virtual_memory."""
    class MockVirtualMemory:
        total = 16000000000  # 16 GB
        available = 8000000000  # 8 GB
        percent = 50.0
        used = 7000000000  # 7 GB
        free = 1000000000  # 1 GB

    monkeypatch.setattr(psutil, "virtual_memory", lambda: MockVirtualMemory)


@pytest.fixture
def mock_swap_memory(monkeypatch):
    """Fixture to mock psutil.swap_memory."""
    class MockSwapMemory:
        total = 8000000000  # 8 GB
        used = 4000000000  # 4 GB
        free = 4000000000  # 4 GB
        percent = 50.0
        sin = 100000000  # 100 MB swapped in
        sout = 50000000   # 50 MB swapped out

    monkeypatch.setattr(psutil, "swap_memory", lambda: MockSwapMemory)


# Test cases
def test_get_virtual_memory(mock_virtual_memory):
    """Test get_virtual_memory."""
    result = Memory.get_virtual_memory()
    expected = {
        'total': 16000000000,
        'available': 8000000000,
        'used': 7000000000,
        'free': 1000000000,
        'percent': 50.0
    }
    assert result == expected

def test_get_swap_memory(mock_swap_memory):
    """Test get_swap_memory."""
    result = Memory.get_swap_memory()
    expected = {
        'total': 8000000000,
        'used': 4000000000,
        'free': 4000000000,
        'percent': 50.0,
        'sin': 100000000,
        'sout': 50000000
    }
    assert result == expected

def test_get_memory_percent(mock_virtual_memory):
    """Test get_memory_percent."""
    result = Memory.get_memory_percent()
    expected = 50.0
    assert result == expected

def test_get_memory_usage(mock_virtual_memory):
    """Test get_memory_usage."""
    result = Memory.get_memory_usage()
    expected = 7000000000  # 7 GB
    assert result == expected

def test_get_memory_available(mock_virtual_memory):
    """Test get_memory_available."""
    result = Memory.get_memory_available()
    expected = 8000000000  # 8 GB
    assert result == expected

def test_get_memory_total(mock_virtual_memory):
    """Test get_memory_total."""
    result = Memory.get_memory_total()
    expected = 16000000000  # 16 GB
    assert result == expected

# Edge Case: Virtual memory with no available memory
def test_virtual_memory_no_available(mock_virtual_memory, monkeypatch):
    """Test virtual memory with no available memory."""
    class MockVirtualMemory:
        total = 16000000000
        available = 0
        percent = 100.0
        used = 16000000000
        free = 0

    monkeypatch.setattr(psutil, "virtual_memory", lambda: MockVirtualMemory)
    result = Memory.get_virtual_memory()
    expected = {
        'total': 16000000000,
        'available': 0,
        'used': 16000000000,
        'free': 0,
        'percent': 100.0
    }
    assert result == expected

# Edge Case: Swap memory with no usage
def test_swap_memory_no_usage(mock_swap_memory, monkeypatch):
    """Test swap memory with no usage."""
    class MockSwapMemory:
        total = 8000000000
        used = 0
        free = 8000000000
        percent = 0.0
        sin = 0
        sout = 0

    monkeypatch.setattr(psutil, "swap_memory", lambda: MockSwapMemory)
    result = Memory.get_swap_memory()
    expected = {
        'total': 8000000000,
        'used': 0,
        'free': 8000000000,
        'percent': 0.0,
        'sin': 0,
        'sout': 0
    }
    assert result == expected

# Edge Case: Virtual memory with high usage but low percentage
def test_virtual_memory_inconsistent_percentage(mock_virtual_memory, monkeypatch):
    """Test virtual memory with high usage but low percentage."""
    class MockVirtualMemory:
        total = 16000000000
        available = 8000000000
        percent = 10.0  # Incorrectly low percentage
        used = 7000000000
        free = 1000000000

    monkeypatch.setattr(psutil, "virtual_memory", lambda: MockVirtualMemory)
    result = Memory.get_virtual_memory()
    expected = {
        'total': 16000000000,
        'available': 8000000000,
        'used': 7000000000,
        'free': 1000000000,
        'percent': 10.0
    }
    assert result == expected


if __name__ == "__main__":
    pytest.main()
