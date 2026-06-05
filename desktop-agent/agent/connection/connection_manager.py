import asyncio
import logging
from enum import Enum
from typing import Optional, Callable, Awaitable

logger = logging.getLogger(__name__)

class ConnectionState(Enum):
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    RECONNECTING = "reconnecting"

class ConnectionManager:
    """
    Manages the WebSocket connection state, reconnection with exponential backoff,
    and notifies the WebSocket client when a connection is established or lost.
    """

    def __init__(
        self,
        url: str,
        on_connect: Optional[Callable[[], Awaitable[None]]] = None,
        on_disconnect: Optional[Callable[[], Awaitable[None]]] = None,
        max_retries: int = 0,            # 0 = infinite
        initial_delay: float = 1.0,
        max_delay: float = 60.0,
        backoff_factor: float = 2.0,
    ):
        self.url = url
        self.on_connect = on_connect
        self.on_disconnect = on_disconnect
        self.max_retries = max_retries
        self.initial_delay = initial_delay
        self.max_delay = max_delay
        self.backoff_factor = backoff_factor

        self.state = ConnectionState.DISCONNECTED
        self._websocket = None
        self._reconnect_task: Optional[asyncio.Task] = None
        self._retry_count = 0

    def is_connected(self) -> bool:
        return self.state == ConnectionState.CONNECTED and self._websocket is not None

    def get_status(self) -> dict:
        return {
            "state": self.state.value,
            "retry_count": self._retry_count,
            "url": self.url,
        }

    async def _reconnect_loop(self, connect_func: Callable[[], Awaitable[None]]):
        """Background task that tries to reconnect on failures."""
        delay = self.initial_delay
        while self.state == ConnectionState.RECONNECTING:
            logger.info(f"Reconnecting in {delay:.1f}s...")
            await asyncio.sleep(delay)

            try:
                await connect_func()
                # Connection succeeded
                self._retry_count = 0
                self.state = ConnectionState.CONNECTED
                if self.on_connect:
                    await self.on_connect()
                return
            except Exception as e:
                self._retry_count += 1
                logger.error(f"Reconnect attempt {self._retry_count} failed: {e}")

                if self.max_retries > 0 and self._retry_count >= self.max_retries:
                    logger.critical("Max reconnect retries reached. Giving up.")
                    self.state = ConnectionState.DISCONNECTED
                    return

                # Exponential backoff
                delay = min(delay * self.backoff_factor, self.max_delay)

    async def connect(self, connect_func: Callable[[], Awaitable[None]]) -> bool:
        """
        Initiate connection. If it fails, start reconnecting in background.
        Returns True if connection succeeded immediately.
        """
        if self.state != ConnectionState.DISCONNECTED:
            logger.warning(f"Cannot connect while in state {self.state}")
            return False

        self.state = ConnectionState.CONNECTING
        try:
            await connect_func()
            self._retry_count = 0
            self.state = ConnectionState.CONNECTED
            if self.on_connect:
                await self.on_connect()
            return True
        except Exception as e:
            logger.error(f"Initial connection failed: {e}")
            self.state = ConnectionState.RECONNECTING
            self._reconnect_task = asyncio.create_task(self._reconnect_loop(connect_func))
            return False

    async def disconnect(self):
        """Gracefully stop all connection and reconnection attempts."""
        if self._reconnect_task and not self._reconnect_task.done():
            self._reconnect_task.cancel()
            try:
                await self._reconnect_task
            except asyncio.CancelledError:
                pass

        if self._websocket:
            try:
                await self._websocket.close()
            except Exception:
                pass
            self._websocket = None

        self.state = ConnectionState.DISCONNECTED
        if self.on_disconnect:
            await self.on_disconnect()
        logger.info("Disconnected")

    def set_websocket(self, ws):
        """Used by the WebSocket client to store the active connection."""
        self._websocket = ws