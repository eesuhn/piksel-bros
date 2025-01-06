import pygame

from typing import TYPE_CHECKING, Any

from .entity import Entity
from ._constants import FRUIT_W, FRUIT_H, ANIMATION_DELAY

if TYPE_CHECKING:
    from ..game import Camera
    from .player import Player


class Fruit(Entity):
    debug: bool

    def __init__(
        self,
        name: str,
        pos: pygame.Vector2,
        *groups: 'Camera'
    ):

        super().__init__(*groups)

        super().init_moving(
            'assets/sprites/fruits',
            pos,
            FRUIT_W,
            FRUIT_H,
            scale=2
        )

        self.name = name
        self.animation_count = 0
        self.pass_through = True
        self.collectable = True

        if len(groups) > 0 and isinstance(groups[0], pygame.sprite.LayeredUpdates):
            groups[0].change_layer(self, 1)

    def update(self, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

        self.animate()

    def create_v_collision(self) -> tuple[pygame.Rect, pygame.Rect]:
        return super().create_v_collision_rects(
            top_offset=8,
            bottom_offset=2,
            x_offset=14
        )

    def animate(self) -> None:
        sprites = self.sheet[self.name]
        max_animation_count = int(len(sprites) * ANIMATION_DELAY)
        sprite_index = int((self.animation_count // ANIMATION_DELAY) % len(sprites))

        self.animation_count = (self.animation_count + 1) % max_animation_count
        self.image = sprites[sprite_index]
        self.mask = pygame.mask.from_surface(self.image)

        super().draw()

    def check_collisions(self, entity_vel: int) -> None:
        """
        Override to skip rectangular collision checks.
        """
        del entity_vel

    def check_collected(self, player: 'Player') -> bool:
        return pygame.sprite.collide_mask(self, player) is not None
