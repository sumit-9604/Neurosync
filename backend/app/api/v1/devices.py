import logging
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.device import Device

logger = logging.getLogger("devices")
router = APIRouter()

_manager = None

def set_manager(manager):
    global _manager
    _manager = manager


@router.get("/devices")
async def get_devices(db: Session = Depends(get_db)):
    devices = db.query(Device).all()
    result = []
    for device in devices:
        # Check if currently online in memory
        is_online = _manager and _manager.get_device(device.device_id) is not None
        result.append({
            "device_id": device.device_id,
            "hostname": device.hostname,
            "os": device.os,
            "status": "online" if is_online else "offline",
            "last_seen": str(device.last_seen) if device.last_seen else None
        })
    return {"devices": result, "total": len(result)}


@router.get("/devices/{device_id}")
async def get_device(device_id: str, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.device_id == device_id).first()
    if not device:
        return JSONResponse(status_code=404, content={"error": f"Device {device_id} not found"})
    is_online = _manager and _manager.get_device(device_id) is not None
    return {
        "device_id": device.device_id,
        "hostname": device.hostname,
        "os": device.os,
        "status": "online" if is_online else "offline",
        "last_seen": str(device.last_seen) if device.last_seen else None
    }