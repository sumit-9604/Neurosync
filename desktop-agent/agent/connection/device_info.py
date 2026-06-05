import platform
import socket
import uuid
import os

def get_device_id() -> str:
    """Generate a stable unique device ID (based on MAC address and hostname)."""
    # Try to get MAC address
    mac = uuid.getnode()
    if mac != uuid.getnode():
        # Fallback: use hostname + random
        return socket.gethostname()
    return str(uuid.UUID(int=mac))

def get_device_info() -> dict:
    """Return a dict with device identification and system details."""
    return {
        "device_id": get_device_id(),
        "hostname": socket.gethostname(),
        "os": platform.system(),
        "os_version": platform.release(),
        "architecture": platform.machine(),
        "cpu_count": os.cpu_count(),
        "python_version": platform.python_version(),
    }