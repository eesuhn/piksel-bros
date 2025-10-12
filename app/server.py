import asyncio
import json
import logging
import websockets

from dataclasses import dataclass, asdict
from typing import Dict, Set, Any
from pathlib import Path


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class PlayerState:
    """Player state data"""

    player_id: str
    name: str
    x: float
    y: float
    vel_x: float
    vel_y: float
    direction: str
    animation_state: str
    is_dashing: bool


class GameServer:
    def __init__(self, level_file: str = "01"):
        self.clients: Dict[str, Any] = {}
        self.player_states: Dict[str, PlayerState] = {}
        self.level_file = level_file
        self.collectibles: Set[str] = set()
        self.load_level()

    def load_level(self):
        """Load level data to track collectibles"""
        try:
            level_path = Path("app/levels") / f"{self.level_file}.json"
            with open(level_path, "r") as f:
                data = json.load(f)
                self.collectibles = set(data.get("fruit", {}).keys())
                logger.info(
                    f"Loaded level {self.level_file} with {len(self.collectibles)} collectibles"
                )
        except Exception as e:
            logger.error(f"Failed to load level: {e}")
            self.collectibles = set()

    async def register(self, websocket: Any, player_id: str, player_name: str):
        """Register a new client"""
        self.clients[player_id] = websocket
        logger.info(
            f"Player {player_id} ({player_name}) connected. Total players: {len(self.clients)}"
        )

        # Send current game state to new player
        await self.send_game_state(websocket)

        # Notify all clients about new player
        await self.broadcast(
            {
                "type": "player_joined",
                "player_id": player_id,
                "player_name": player_name,
                "total_players": len(self.clients),
            }
        )

    async def unregister(self, player_id: str):
        """Unregister a client"""
        if player_id in self.clients:
            del self.clients[player_id]
        if player_id in self.player_states:
            del self.player_states[player_id]

        logger.info(
            f"Player {player_id} disconnected. Total players: {len(self.clients)}"
        )

        # Notify remaining clients
        await self.broadcast(
            {
                "type": "player_left",
                "player_id": player_id,
                "total_players": len(self.clients),
            }
        )

    async def send_game_state(self, websocket: Any):
        """Send current game state to a specific client"""
        state = {
            "type": "game_state",
            "players": {
                pid: asdict(state) for pid, state in self.player_states.items()
            },
            "collectibles": list(self.collectibles),
        }
        await websocket.send(json.dumps(state))

    async def broadcast(self, message: dict, exclude: str = None):
        """Broadcast message to all connected clients"""
        if not self.clients:
            return

        message_str = json.dumps(message)
        disconnected = []

        for player_id, websocket in self.clients.items():
            if player_id == exclude:
                continue
            try:
                await websocket.send(message_str)
            except websockets.exceptions.ConnectionClosed:
                disconnected.append(player_id)

        # Clean up disconnected clients
        for player_id in disconnected:
            await self.unregister(player_id)

    async def handle_position_update(self, player_id: str, data: dict):
        """Handle player position update"""
        self.player_states[player_id] = PlayerState(
            player_id=player_id,
            name=data.get("name", "Player"),
            x=data["x"],
            y=data["y"],
            vel_x=data.get("vel_x", 0),
            vel_y=data.get("vel_y", 0),
            direction=data.get("direction", "right"),
            animation_state=data.get("animation_state", "IDLE"),
            is_dashing=data.get("is_dashing", False),
        )

        # Broadcast to other players
        await self.broadcast(
            {
                "type": "player_update",
                "player_id": player_id,
                "data": asdict(self.player_states[player_id]),
            },
            exclude=player_id,
        )

    async def handle_collectible(self, player_id: str, data: dict):
        """Handle collectible pickup"""
        collectible_key = data.get("key")
        if collectible_key in self.collectibles:
            self.collectibles.remove(collectible_key)
            logger.info(
                f"Player {player_id} collected {collectible_key}. Remaining: {len(self.collectibles)}"
            )

            # Broadcast to all players
            await self.broadcast(
                {
                    "type": "collectible_picked",
                    "player_id": player_id,
                    "key": collectible_key,
                    "remaining": len(self.collectibles),
                }
            )

            # Check win condition
            if len(self.collectibles) == 0:
                await self.broadcast({"type": "game_won", "winner_id": player_id})

    async def handle_message(self, websocket: Any, message: str):
        """Handle incoming message from client"""
        try:
            data = json.loads(message)
            msg_type = data.get("type")
            player_id = data.get("player_id")

            if msg_type == "connect":
                await self.register(websocket, player_id, data.get("name", "Player"))

            elif msg_type == "position":
                await self.handle_position_update(player_id, data)

            elif msg_type == "collectible":
                await self.handle_collectible(player_id, data)

            elif msg_type == "ping":
                await websocket.send(json.dumps({"type": "pong"}))

        except json.JSONDecodeError:
            logger.error(f"Invalid JSON received: {message}")
        except Exception as e:
            logger.error(f"Error handling message: {e}")

    async def handle_client(self, websocket: Any):
        """Handle a client connection"""
        player_id = None
        try:
            async for message in websocket:
                if not player_id and "player_id" in message:
                    data = json.loads(message)
                    player_id = data.get("player_id")

                await self.handle_message(websocket, message)

        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Connection closed for player {player_id}")
        except Exception as e:
            logger.error(f"Error in handle_client: {e}")
        finally:
            if player_id:
                await self.unregister(player_id)

    async def start(self, host: str = "localhost", port: int = 8765):
        """Start the WebSocket server"""
        logger.info(f"Starting server on ws://{host}:{port}")
        async with websockets.serve(self.handle_client, host, port):
            await asyncio.Future()  # Run forever


if __name__ == "__main__":
    server = GameServer(level_file="01")
    asyncio.run(server.start())
