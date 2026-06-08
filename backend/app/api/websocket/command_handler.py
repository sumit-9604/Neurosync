import logging
import json
from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.api.websocket.connection_manager import ConnectionManager
from app.models.device import Device
from app.db.database import SessionLocal

logger = logging.getLogger("command_handler")
router = APIRouter()

_manager: ConnectionManager = None

def set_manager(manager: ConnectionManager):
    global _manager
    _manager = manager


class CommandRequest(BaseModel):
    device_id: str
    action: str
    payload: dict = {}


def _save_device_to_db(device_id: str, hostname: str, os: str = None, os_version: str = None):
    db = SessionLocal()
    try:
        device = db.query(Device).filter(Device.device_id == device_id).first()
        if device:
            device.status = "online"
            device.hostname = hostname
        else:
            device = Device(
                device_id=device_id,
                hostname=hostname,
                os=os,
                os_version=os_version,
                status="online"
            )
            db.add(device)
        db.commit()
        logger.info(f"Device saved to DB: {device_id}")
    except Exception as e:
        logger.error(f"Failed to save device to DB: {e}")
        db.rollback()
    finally:
        db.close()


def _set_device_offline(device_id: str):
    db = SessionLocal()
    try:
        device = db.query(Device).filter(Device.device_id == device_id).first()
        if device:
            device.status = "offline"
            db.commit()
            logger.info(f"Device set offline in DB: {device_id}")
    except Exception as e:
        logger.error(f"Failed to update device status: {e}")
        db.rollback()
    finally:
        db.close()


async def handle_agent_connection(websocket: WebSocket, manager: ConnectionManager):
    global _manager
    _manager = manager

    device_id = None
    try:
        await websocket.accept()
        raw = await websocket.receive_text()
        data = json.loads(raw)

        device_id = data.get("device_id")
        hostname = data.get("hostname", "unknown")
        os = data.get("os")
        os_version = data.get("os_version")

        if not device_id:
            await websocket.send_json({"error": "device_id required"})
            await websocket.close()
            return

        # Register in memory
        manager.connected_agents[device_id] = websocket
        logger.info(f"Agent registered: {device_id} ({hostname})")

        # ✅ Save to DB
        _save_device_to_db(device_id, hostname, os, os_version)

        await websocket.send_json({
            "type": "registered",
            "device_id": device_id,
            "message": "Connected to NeuroSync backend"
        })

        while True:
            text = await websocket.receive_text()
            msg = json.loads(text)
            msg_type = msg.get("type")

            if msg_type == "heartbeat":
                await websocket.send_json({"type": "heartbeat_ack"})
                logger.debug(f"Heartbeat from {device_id}")

            elif msg_type == "command_result":
                logger.info(f"Result from {device_id}: {msg}")

            else:
                logger.warning(f"Unknown message type from {device_id}: {msg_type}")

    except WebSocketDisconnect:
        logger.info(f"Agent disconnected: {device_id}")
    except Exception as e:
        logger.error(f"Error in agent connection: {e}")
    finally:
        if device_id:
            manager.disconnect(device_id)
            # ✅ Mark offline in DB
            _set_device_offline(device_id)


@router.post("/command")
async def send_command(req: CommandRequest):
    if _manager is None:
        return JSONResponse(status_code=503, content={"error": "Manager not initialized"})

    sent = await _manager.send_to_device(req.device_id, {
        "type": "command",
        "action": req.action,
        "payload": req.payload
    })

    if not sent:
        return JSONResponse(status_code=404, content={"error": f"Device {req.device_id} not connected"})

    return {"status": "sent", "device_id": req.device_id, "action": req.action}