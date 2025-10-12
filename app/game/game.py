"""
app/game/game.py (Modified for Multiplayer)
Replace your existing game.py with this version
"""

import pygame
import sys
import justsdk

from .._constants import SCR_W, SCR_H, FPS
from .level import Level
from .camera import Camera
from .background import Background
from .network_manager import NetworkManager
from ..entities import Player
from ..entities.remote_player import RemotePlayer
from ..entities._constants import PLAYER_H
from ._constants import SCR_FLAGS


class Game:
    def __init__(self, multiplayer: bool = False, player_name: str = "Player"):
        pygame.init()
        pygame.display.set_caption("Piksel Bros.")

        self.screen = pygame.display.set_mode((SCR_W, SCR_H), SCR_FLAGS)
        self.display = pygame.Surface((SCR_W, SCR_H)).convert_alpha()

        # Multiplayer setup
        self.multiplayer = multiplayer
        self.player_name = player_name
        self.network_manager = None
        self.remote_players = {}  # player_id -> RemotePlayer
        self.position_update_counter = 0
        self.position_update_rate = 2  # Send position every N frames

    def run(self, debug: bool = False) -> None:
        self.debug = debug
        self.win = False
        self.clock = pygame.time.Clock()

        # Initialize network BEFORE loading level if multiplayer
        if self.multiplayer:
            self._init_network()

        self.load_level()

        while True:
            self.check_events()
            self.loop()
            self.clock.tick(FPS)

    def _init_network(self) -> None:
        """Initialize network manager and set up callbacks"""
        self.network_manager = NetworkManager(self.player_name)

        # Set up callbacks
        self.network_manager.on_player_update = self._on_player_update
        self.network_manager.on_player_joined = self._on_player_joined
        self.network_manager.on_player_left = self._on_player_left
        self.network_manager.on_collectible_picked = self._on_collectible_picked
        self.network_manager.on_game_state = self._on_game_state
        self.network_manager.on_game_won = self._on_game_won

        # Start network thread
        self.network_manager.start()
        justsdk.print_info(
            f"Multiplayer enabled! Player ID: {self.network_manager.player_id}"
        )

    def _on_player_update(self, data: dict) -> None:
        """Handle remote player position update"""
        player_id = data["player_id"]
        player_data = data["data"]

        if player_id not in self.remote_players:
            # Create new remote player
            self._create_remote_player(player_data)
        else:
            # Update existing remote player
            self.remote_players[player_id].update_from_network(player_data)

    def _on_player_joined(self, data: dict) -> None:
        """Handle new player joining"""
        player_id = data["player_id"]
        player_name = data["player_name"]
        justsdk.print_info(
            f"{player_name} ({player_id}) joined the game! Total players: {data['total_players']}"
        )

    def _on_player_left(self, data: dict) -> None:
        """Handle player leaving"""
        player_id = data["player_id"]
        if player_id in self.remote_players:
            self.remote_players[player_id].kill()
            self.objs.remove(self.remote_players[player_id])
            del self.remote_players[player_id]
        justsdk.print_info(f"Player left. Total players: {data['total_players']}")

    def _on_collectible_picked(self, data: dict) -> None:
        """Handle collectible picked by any player"""
        key = data["key"]

        # Remove collectible from local game
        for obj in self.objs[:]:  # Create copy to avoid modification during iteration
            if obj.collectable and hasattr(obj, "name"):
                # Match collectible by grid position
                obj_key = f"{int(obj.rect.x // 64)};{int(obj.rect.y // 64)}"
                if obj_key == key:
                    obj.kill()
                    self.objs.remove(obj)
                    break

    def _on_game_state(self, data: dict) -> None:
        """Handle initial game state from server"""
        # Create remote players for existing players
        for player_id, player_data in data["players"].items():
            if player_id != self.network_manager.player_id:
                self._create_remote_player(player_data)

    def _on_game_won(self, data: dict) -> None:
        """Handle game won event"""
        winner_id = data["winner_id"]
        if winner_id == self.network_manager.player_id:
            justsdk.print_info("You won!")
        else:
            justsdk.print_info("Another player won the game!")
        self.win = True

    def _create_remote_player(self, player_data: dict) -> None:
        """Create a remote player entity"""
        player_id = player_data["player_id"]

        if player_id in self.remote_players:
            return

        # Remote player uses world coordinates directly (not grid coordinates)
        # We'll set the position after creation
        remote_player = RemotePlayer(
            player_id=player_id,
            name=player_data["name"],
            character_name=self.level.get_player_name(),  # Use same character
            pos=pygame.Vector2(0, 0),  # Temporary position, will be updated immediately
            camera=self.camera,
        )

        # Set the actual position from network data
        remote_player.rect.x = player_data["x"]
        remote_player.rect.y = player_data["y"]
        remote_player.target_pos.x = player_data["x"]
        remote_player.target_pos.y = player_data["y"]
        remote_player.update_from_network(player_data)

        self.remote_players[player_id] = remote_player
        self.objs.append(remote_player)
        self.camera.add(remote_player)

    def check_events(self) -> None:
        self.events = pygame.event.get()

        for event in self.events:
            if event.type == pygame.QUIT:
                self._end()
            if event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)

    def handle_keydown(self, key: int) -> None:
        if key == pygame.K_ESCAPE:
            self._end()

    def _end(self) -> None:
        if self.network_manager:
            self.network_manager.disconnect()
        pygame.quit()
        sys.exit()

    def loop(self) -> None:
        """Main loop of the game."""
        self.display.fill((0, 0, 0))

        self.camera.update(
            events=self.events,
            display=self.display,
            objs=[
                o for o in self.objs if not isinstance(o, RemotePlayer)
            ],  # Exclude remote players from collision
            top_left=self.top_left,
            bottom_right=self.bottom_right,
            debug=self.debug,
            set_border=True,
            camera_delay=True,
        )

        # Send position updates in multiplayer mode
        if self.multiplayer and self.network_manager and self.network_manager.connected:
            self._send_position_update()

        self._check_state()

        self.screen.blit(
            pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)
        )
        pygame.display.update()

    def _send_position_update(self) -> None:
        """Send player position to server"""
        self.position_update_counter += 1

        if self.position_update_counter >= self.position_update_rate:
            self.network_manager.send_position(
                x=float(self.player.rect.x),
                y=float(self.player.rect.y),
                vel_x=float(self.player.vel.x),
                vel_y=float(self.player.vel.y),
                direction=self.player.direction,
                animation_state=self.player.animation_state.name,
                is_dashing=self.player.is_dashing,
            )
            self.position_update_counter = 0

    def load_level(self) -> None:
        self.level = Level("01")

        level_w, level_h = self.level.get_dimensions()
        self.top_left = self.level.get_top_left()
        self.bottom_right = self.level.get_bottom_right()

        self.camera = Camera(level_w, level_h)

        # Get player position from level (same for all players for now)
        player_pos = self.level.get_player_pos()

        if self.multiplayer:
            justsdk.print_info(f"Multiplayer mode - spawn at: {player_pos}")

        self.player = Player(self.level.get_player_name(), player_pos, self.camera)
        self.objs = self.level.load(self.camera, self.player)

        # Debug: Print terrain around spawn
        if self.multiplayer:
            justsdk.print_info(f"Total objects loaded: {len(self.objs)}")
            terrain_count = sum(
                1 for o in self.objs if hasattr(o, "name") and not o.collectable
            )
            justsdk.print_info(f"Terrain blocks: {terrain_count}")

        # No background in debug mode
        if not self.debug:
            self.background = Background(self.camera)
            self.background.add_target(self.player)

    def _check_state(self) -> None:
        """Monitor the state of the game."""
        self._check_collectables()
        self._check_win()
        self._check_fallen()

    def _check_collectables(self) -> None:
        """Update and check if all collectables have been collected."""
        for obj in [o for o in self.objs if o.collectable]:
            if obj.check_collected(self.player):
                # Calculate grid position for network sync
                grid_x = int(obj.rect.x // 64)
                grid_y = int(obj.rect.y // 64)
                key = f"{grid_x};{grid_y}"

                # Notify server in multiplayer mode
                if self.multiplayer and self.network_manager:
                    self.network_manager.send_collectible(key)

                obj.kill()
                self.objs.remove(obj)

    def _check_win(self) -> None:
        """Monitor winning condition(s)."""
        if not any(o.collectable for o in self.objs) and not self.win:
            justsdk.print_info("You won!")
            self.win = True

    def _check_fallen(self) -> None:
        """Check if the player has fallen out of the map."""
        fall_limit = self.bottom_right.y + (PLAYER_H * 10)
        if self.player.rect.top > fall_limit:
            justsdk.print_info(
                f"You fell out of the map! Player Y: {self.player.rect.top}, Limit: {fall_limit}"
            )
            self._end()
