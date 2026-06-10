import uuid
import socket
import platform
import getpass
import psutil

def get_device_info() -> dict:
    # Get primary local IP
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
    except Exception:
        ip = "unknown"

    # Get MAC address
    try:
        import uuid as _uuid
        mac = ':'.join([
            '{:02x}'.format((uuid.getnode() >> i) & 0xff)
            for i in range(0, 48, 8)
        ][::-1])
    except Exception:
        mac = "unknown"

    # CPU and RAM
    try:
        cpu = platform.processor() or "unknown"
        ram_gb = str(round(psutil.virtual_memory().total / (1024 ** 3), 1))
    except Exception:
        cpu = "unknown"
        ram_gb = "unknown"

    return {
        "device_id":   str(uuid.getnode()),          # stable hardware-based ID
        "hostname":    socket.gethostname(),
        "username":    getpass.getuser(),             # Windows login name
        "os":          platform.system(),
        "os_version":  platform.version(),
        "ip_address":  ip,
        "mac_address": mac,
        "cpu":         cpu,
        "ram_gb":      ram_gb,
    }