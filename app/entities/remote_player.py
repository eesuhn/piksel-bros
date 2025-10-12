"""
app/entities/remote_player.py
Remote player entity for displaying other players
"""

import pygame
from typing import TYPE_CHECKING, Any

from .entity import Entity
from ._constants import PLAYER_W, PLAYER_H, ANIMATION_DELAY

if TYPE_CHECKING:
    from ..game import Camera


class RemotePlayer(Entity):
    """Represents a remote player controlled by another client"""

    display: pygame.Surface
    debug: bool

    def __init__(
        self,
        player_id: str,
        name: str,
        character_name: str,
        pos: pygame.Vector2,
        camera: "Camera",  # Changed from *groups to explicit camera parameter
    ):
        super().__init__(
            camera
        )  # Pass camera to parent (Entity which inherits from Sprite)

        self.pass_through = True  # Remote players don't collide with local player
        self.collectable = False

        super().init_moving(
            f"assets/sprites/characters/{character_name}",
            pos,
            PLAYER_W,
            PLAYER_H,
            scale=2,
            direction=True,
        )

        self.player_id = player_id
        self.name = name
        self.character_name = character_name
        self.vel = pygame.Vector2(0, 0)
        self.direction = "right"
        self.animation_state = "IDLE"
        self.animation_count = 0
        self.is_dashing = False
        self.debug = False

        # Interpolation for smooth movement
        self.target_pos = pygame.Vector2(pos.x * PLAYER_W * 2, pos.y * PLAYER_H * 2)
        self.interpolation_speed = 0.3

        # Name label
        self.font = pygame.font.Font(None, 20)
        self.name_label = self.font.render(self.name, True, (255, 255, 255))
        self.name_outline = self.font.render(self.name, True, (0, 0, 0))

        if camera and isinstance(camera, pygame.sprite.LayeredUpdates):
            camera.change_layer(self, 1)

    def update(self, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

        if self.debug:
            super().debug_hitboxes()

        self._interpolate_position()
        self._animate()
        self._draw_name_label()

    def update_from_network(self, data: dict) -> None:
        """Update player state from network data"""
        self.target_pos.x = data["x"]
        self.target_pos.y = data["y"]
        self.vel.x = data.get("vel_x", 0)
        self.vel.y = data.get("vel_y", 0)
        self.direction = data.get("direction", "right")
        self.animation_state = data.get("animation_state", "IDLE")
        self.is_dashing = data.get("is_dashing", False)

    def _interpolate_position(self) -> None:
        """Smoothly interpolate position towards target"""
        diff_x = self.target_pos.x - self.rect.x
        diff_y = self.target_pos.y - self.rect.y

        self.rect.x += int(diff_x * self.interpolation_speed)
        self.rect.y += int(diff_y * self.interpolation_speed)

        self._update_hitboxes()

    def _animate(self) -> None:
        """Animate the remote player"""
        sheet_name = f"{self.animation_state.lower()}_{self.direction}"

        # Fallback to idle if animation state doesn't exist
        if sheet_name not in self.sheet:
            sheet_name = f"idle_{self.direction}"

        sprites = self.sheet[sheet_name]

        max_animation_count = int(len(sprites) * ANIMATION_DELAY)
        sprite_index = int((self.animation_count // ANIMATION_DELAY) % len(sprites))

        self.animation_count = (self.animation_count + 1) % max_animation_count
        self.image = sprites[sprite_index]

        # Add dash effect if dashing
        if self.is_dashing:
            self.image = self.image.copy()
            self.image.set_alpha(200)

        super().draw()

    def _draw_name_label(self) -> None:
        """Draw player name above their head"""
        label_x = self.rect.centerx - self.name_label.get_width() // 2
        label_y = self.rect.top - 20

        # Draw outline
        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            self.display.blit(
                self.name_outline,
                (
                    label_x + dx - self.offset.x - self.top_left.x,
                    label_y + dy - self.offset.y - self.top_left.y,
                ),
            )

        # Draw name
        self.display.blit(
            self.name_label,
            (
                label_x - self.offset.x - self.top_left.x,
                label_y - self.offset.y - self.top_left.y,
            ),
        )

    def create_v_collision(self) -> tuple[pygame.Rect, pygame.Rect]:
        return super().create_v_collision_rects(
            top_offset=8, bottom_offset=2, x_offset=14
        )

    def check_collisions(self, entity_vel: int) -> None:
        """Remote players don't need collision detection with terrain"""
        pass

    def _apply_gravity(self) -> None:
        """Remote players don't use gravity - position comes from network"""
        pass
