import asyncio
import logging
from typing import Optional, Callable, Awaitable

logger = logging.getLogger(__name__)

class Heartbeat:
    """
    Send periodic heartbeat messages over a WebSocket.
    The heartbeat task runs independently and can be cancelled.
    """

    def __init__(
        self,
        send_callback: Callable[[dict], Awaitable[None]],
        device_id: str,
        interval: int = 30,
    ):
        self.send_callback = send_callback
        self.device_id = device_id
        self.interval = interval
        self._task: Optional[asyncio.Task] = None
        self._running = False

    async def _run(self):
        """Internal loop sending heartbeats."""
        while self._running:
            try:
                await asyncio.sleep(self.interval)
                await self.send_callback({
                    "type": "heartbeat",
                    "device_id": self.device_id,
                    "timestamp": asyncio.get_event_loop().time()
                })
                logger.debug("Heartbeat sent")
            except Exception as e:
                logger.warning(f"Heartbeat send failed: {e}")

    def start(self):
        """Start the heartbeat task."""
        if self._task is None or self._task.done():
            self._running = True
            self._task = asyncio.create_task(self._run())
            logger.info(f"Heartbeat started (interval={self.interval}s)")

    async def stop(self):
        """Stop the heartbeat task gracefully."""
        self._running = False
        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("Heartbeat stopped")