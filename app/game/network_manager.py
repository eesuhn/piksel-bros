import asyncio
import json
import threading
import uuid
import logging

from typing import Callable, Optional

try:
    import websockets
except ImportError:
    print("Installing websockets...")
    import subprocess

    subprocess.check_call(["pip", "install", "websockets"])
    import websockets

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NetworkManager:
    def __init__(self, player_name: str, server_url: str = "ws://localhost:8765"):
        self.player_id = str(uuid.uuid4())[:8]
        self.player_name = player_name
        self.server_url = server_url
        self.websocket = None
        self.connected = False
        self.loop = None
        self.thread = None

        # Callbacks
        self.on_player_update: Optional[Callable] = None
        self.on_player_joined: Optional[Callable] = None
        self.on_player_left: Optional[Callable] = None
        self.on_collectible_picked: Optional[Callable] = None
        self.on_game_state: Optional[Callable] = None
        self.on_game_won: Optional[Callable] = None

    def start(self):
        """Start the network manager in a separate thread"""
        self.thread = threading.Thread(target=self._run_event_loop, daemon=True)
        self.thread.start()
        logger.info(f"Network manager started for player {self.player_id}")

    def _run_event_loop(self):
        """Run the asyncio event loop in a separate thread"""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self._connect())

    async def _connect(self):
        """Connect to the WebSocket server"""
        try:
            async with websockets.connect(self.server_url) as websocket:
                self.websocket = websocket
                self.connected = True
                logger.info(f"Connected to server at {self.server_url}")

                # Send initial connection message
                await self._send(
                    {
                        "type": "connect",
                        "player_id": self.player_id,
                        "name": self.player_name,
                    }
                )

                # Listen for messages
                async for message in websocket:
                    await self._handle_message(message)

        except Exception as e:
            logger.error(f"Connection error: {e}")
            self.connected = False

    async def _send(self, data: dict):
        """Send data to the server"""
        if self.websocket and self.connected:
            try:
                await self.websocket.send(json.dumps(data))
            except Exception as e:
                logger.error(f"Send error: {e}")
                self.connected = False

    def send_position(
        self,
        x: float,
        y: float,
        vel_x: float,
        vel_y: float,
        direction: str,
        animation_state: str,
        is_dashing: bool,
    ):
        """Send player position update to server"""
        if not self.connected:
            return

        data = {
            "type": "position",
            "player_id": self.player_id,
            "name": self.player_name,
            "x": x,
            "y": y,
            "vel_x": vel_x,
            "vel_y": vel_y,
            "direction": direction,
            "animation_state": animation_state,
            "is_dashing": is_dashing,
        }

        # Schedule send in the network thread
        if self.loop:
            asyncio.run_coroutine_threadsafe(self._send(data), self.loop)

    def send_collectible(self, key: str):
        """Notify server that a collectible was picked up"""
        if not self.connected:
            return

        data = {"type": "collectible", "player_id": self.player_id, "key": key}

        if self.loop:
            asyncio.run_coroutine_threadsafe(self._send(data), self.loop)

    async def _handle_message(self, message: str):
        """Handle incoming message from server"""
        try:
            data = json.loads(message)
            msg_type = data.get("type")

            if msg_type == "player_update" and self.on_player_update:
                self.on_player_update(data)

            elif msg_type == "player_joined" and self.on_player_joined:
                self.on_player_joined(data)

            elif msg_type == "player_left" and self.on_player_left:
                self.on_player_left(data)

            elif msg_type == "collectible_picked" and self.on_collectible_picked:
                self.on_collectible_picked(data)

            elif msg_type == "game_state" and self.on_game_state:
                self.on_game_state(data)

            elif msg_type == "game_won" and self.on_game_won:
                self.on_game_won(data)

        except Exception as e:
            logger.error(f"Error handling message: {e}")

    def disconnect(self):
        """Disconnect from the server"""
        self.connected = False
        if self.loop:
            self.loop.stop()
        logger.info("Disconnected from server")
