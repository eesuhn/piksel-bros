import pygame

from typing import TYPE_CHECKING, Any
from enum import Enum, auto

from .entity import Entity
from ._constants import PLAYER_W, PLAYER_H, ANIMATION_DELAY, PLAYER_VEL

if TYPE_CHECKING:
    from ..game import Camera


class Player(Entity):
    def __init__(self, name: str, pos: pygame.Vector2, *groups: 'Camera'):
        super().__init__(*groups)

        self.init_moving_graphics(
            f'assets/images/characters/{name}',
            pos,
            PLAYER_W,
            PLAYER_H,
            scale=2,
            direction=True
        )

        self.vel = pygame.Vector2(0, 0)
        self.head_rect, self.feet_rect = self.create_v_collision()
        self.head_sprite = pygame.sprite.Sprite()
        self.feet_sprite = pygame.sprite.Sprite()
        self.collide_left = False
        self.collide_right = False

        self.direction = 'right'
        self.animation_state = PlayerAnimation.IDLE
        self.animation_count = 0
        self.jump_count = 0
        self.fall_count = 0

        if len(groups) > 0 and isinstance(groups[0], pygame.sprite.LayeredUpdates):
            groups[0].change_layer(self, 1)

    def update(self, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

        self.animate()
        self.handle_input()
        self.apply_movement()

    def handle_input(self) -> None:
        keys = pygame.key.get_pressed()
        self.vel.x = 0

        if keys[pygame.K_LEFT] and not self.collide_left:
            self.move_horizontal(-PLAYER_VEL)
        if keys[pygame.K_RIGHT] and not self.collide_right:
            self.move_horizontal(PLAYER_VEL)

    def get_animation_state(self) -> 'PlayerAnimation':
        if self.vel.y < 0:
            return PlayerAnimation.DOUBLE_JUMP if self.jump_count == 2 else PlayerAnimation.JUMP
        if self.vel.y > 1:
            return PlayerAnimation.FALL
        if self.vel.x != 0:
            return PlayerAnimation.RUN
        return PlayerAnimation.IDLE

    def animate(self) -> None:
        self.animation_state = self.get_animation_state()
        sheet_name = f"{self.animation_state.name.lower()}_{self.direction}"
        sprites = self.sheet[sheet_name]

        max_animation_count = int(len(sprites) * ANIMATION_DELAY)
        sprite_index = int((self.animation_count // ANIMATION_DELAY) % len(sprites))

        self.animation_count = (self.animation_count + 1) % max_animation_count
        self.image = sprites[sprite_index]

        self.draw()

    def create_v_collision(self) -> tuple[pygame.Rect, pygame.Rect]:
        return super().create_v_collision_rects(
            top_offset=8,
            bottom_offset=2,
            x_offset=14
        )


class PlayerAnimation(Enum):
    """
    Enum class to represent the player animation states
    """
    IDLE = auto()
    JUMP = auto()
    DOUBLE_JUMP = auto()
    RUN = auto()
    FALL = auto()
