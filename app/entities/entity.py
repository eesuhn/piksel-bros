import pygame

from typing import TYPE_CHECKING, Callable
from pathlib import Path

from ..utils import load_sprites_sheet, load_image

if TYPE_CHECKING:
    from ..game import Camera


class Entity(pygame.sprite.Sprite):
    display: pygame.Surface
    offset: pygame.Vector2
    top_left: pygame.Vector2
    vel: pygame.Vector2

    # Child callable to include `create_v_collision_rects`
    create_v_collision: Callable

    def __init__(self, *groups: 'Camera'):
        super().__init__(*groups)

    def draw(self) -> None:
        self.display.blit(
            self.image,
            (
                self.rect.x - self.offset.x - self.top_left.x,
                self.rect.y - self.offset.y - self.top_left.y
            )
        )

    def init_moving_graphics(
        self,
        relative_path: str | Path,
        pos: pygame.Vector2,
        width: int,
        height: int,
        scale: int = 1,
        direction: bool = False
    ) -> None:
        """
        Initialize moving graphics for the entity.
        """

        scaled_width = width * scale
        scaled_height = height * scale

        self.rect = pygame.Rect(
            pos.x * scaled_width,
            pos.y * scaled_height,
            scaled_width,
            scaled_height
        )
        self.sheet = load_sprites_sheet(
            relative_path,
            width,
            height,
            scale=scale,
            direction=direction
        )
        self.image = pygame.Surface(
            (scaled_width, scaled_height)
        ).convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

    def init_static_graphics(
        self,
        relative_path: str | Path,
        pos: pygame.Vector2,
        width: int,
        height: int,
        scale: int = 1
    ) -> None:
        """
        Initialize static graphics for the entity.
        """

        scaled_width = width * scale
        scaled_height = height * scale

        self.rect = pygame.Rect(
            pos.x * scaled_width,
            pos.y * scaled_height,
            scaled_width,
            scaled_height
        )
        self.image = load_image(relative_path)
        self.mask = pygame.mask.from_surface(self.image)

    def create_v_collision_rects(
        self,
        top_offset: int,
        bottom_offset: int,
        x_offset: int = 0
    ) -> tuple[pygame.Rect, pygame.Rect]:
        """
        Create vertical collision rects.
        """

        def create_rect(
            x_offset: int,
            y_offset: int
        ) -> pygame.Rect:
            width = self.rect.width - (x_offset * 2)
            height = 2
            return pygame.Rect(
                self.rect.x + x_offset,
                self.rect.y + y_offset,
                width,
                height
            )

        top_rect = create_rect(x_offset, top_offset)
        bottom_rect = create_rect(
            x_offset,
            self.rect.height - bottom_offset
        )

        return top_rect, bottom_rect

    def move_horizontal(self, speed: int = 1) -> None:
        self.vel.x = speed
        self.direction = 'right' if speed > 0 else 'left'

    def apply_movement(self) -> None:
        self.rect.move_ip(self.vel.x, self.vel.y)
        self.update_hitboxes()

    def update_hitboxes(self) -> None:
        self.mask = pygame.mask.from_surface(self.image)
        self.head_rect, self.feet_rect = self.create_v_collision()
