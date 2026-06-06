import logging
import json
from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from app.api.websocket.connection_manager import ConnectionManager

logger = logging.getLogger("terminal_handler")
router = APIRouter()


async def handle_terminal_command(
    device_id: str,
    command: str,
    manager: ConnectionManager,
    mobile_ws: WebSocket
):
    """
    Send a terminal command to a desktop agent and
    stream output back to the mobile client.
    """
    sent = await manager.send_to_device(device_id, {
        "type": "terminal_command",
        "command": command
    })

    if not sent:
        await mobile_ws.send_json({
            "type": "error",
            "message": f"Device {device_id} not connected"
        })
        return

    logger.info(f"Terminal command sent to {device_id}: {command}")