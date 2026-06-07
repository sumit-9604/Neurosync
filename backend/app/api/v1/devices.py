import logging
from fastapi import APIRouter
from fastapi.responses import JSONResponse

logger = logging.getLogger("devices")
router = APIRouter()

# Import shared manager — set after app starts
_manager = None

def set_manager(manager):
    global _manager
    _manager = manager


@router.get("/devices")
async def get_devices():
    if _manager is None:
        return JSONResponse(status_code=503, content={"error": "Manager not ready"})

    devices = []
    for device_id in _manager.get_all_devices():
        devices.append({
            "device_id": device_id,
            "status": "online"
        })
        logger.info(
        f"Devices API sees: {_manager.get_all_devices()}"
    )


    return {"devices": devices, "total": len(devices)}


@router.get("/devices/{device_id}")
async def get_device(device_id: str):
    if _manager is None:
        return JSONResponse(status_code=503, content={"error": "Manager not ready"})

    ws = _manager.get_device(device_id)
    if not ws:
        return JSONResponse(status_code=404, content={"error": f"Device {device_id} not found"})

    return {"device_id": device_id, "status": "online"}