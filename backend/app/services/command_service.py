import logging
from app.api.websocket.connection_manager import ConnectionManager

logger = logging.getLogger("command_service")


class CommandService:
    def __init__(self, manager: ConnectionManager):
        self.manager = manager

    async def execute(self, device_id: str, action: str, payload: dict = {}) -> dict:
        if not self.manager.get_device(device_id):
            logger.warning(f"Command failed — device offline: {device_id}")
            return {"status": "error", "message": f"Device {device_id} not connected"}

        sent = await self.manager.send_to_device(device_id, {
            "type": "command",
            "action": action,
            "payload": payload
        })

        if sent:
            logger.info(f"Command sent — device: {device_id}, action: {action}")
            return {"status": "sent", "device_id": device_id, "action": action}
        else:
            return {"status": "error", "message": "Failed to send command"}