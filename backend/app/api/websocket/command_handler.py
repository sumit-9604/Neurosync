import logging
import json
from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.api.websocket.connection_manager import ConnectionManager

logger = logging.getLogger("command_handler")
router = APIRouter()

# Add this function near the top of command_handler.py
def set_manager(manager: ConnectionManager):
    global _manager
    _manager = manager
_manager: ConnectionManager = None


class CommandRequest(BaseModel):
    device_id: str
    action: str
    payload: dict = {}


async def handle_agent_connection(websocket: WebSocket, manager: ConnectionManager):
    global _manager
    _manager = manager

    device_id = None
    try:
        # Step 1: Accept raw connection first to read registration message
        await websocket.accept()
        raw = await websocket.receive_text()
        data = json.loads(raw)

        device_id = data.get("device_id")
        hostname = data.get("hostname", "unknown")

        if not device_id:
            await websocket.send_json({"error": "device_id required"})
            await websocket.close()
            return

        # Register without calling accept() again
        manager.connected_agents[device_id] = websocket
        logger.info(f"Agent registered: {device_id} ({hostname})")

        await websocket.send_json({
            "type": "registered",
            "device_id": device_id,
            "message": "Connected to NeuroSync backend"
        })

        # Step 2: Listen for incoming messages (heartbeats, results)
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