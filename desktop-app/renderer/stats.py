import psutil
import json
import sys
import time

while True:
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent if sys.platform != 'win32' else psutil.disk_usage('C:\\').percent
    net = psutil.net_io_counters()
    
    data = {
        "cpu": cpu,
        "ram": ram,
        "disk": disk,
        "net_sent": round(net.bytes_sent / 1024 / 1024, 2),
        "net_recv": round(net.bytes_recv / 1024 / 1024, 2),
        "procs": len(psutil.pids()),
        "hostname": psutil.os.uname().nodename if hasattr(psutil.os, 'uname') else "UNKNOWN"
    }
    print(json.dumps(data), flush=True)
    time.sleep(2)