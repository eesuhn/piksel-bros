import pygame

from typing import TYPE_CHECKING
from pathlib import Path

from ..utils import load_sprites_sheet, load_image

if TYPE_CHECKING:
    from ..game import Camera


class Entity(pygame.sprite.Sprite):
    display: pygame.Surface
    image: pygame.Surface
    rect: pygame.Rect
    offset: pygame.Vector2
    top_left: pygame.Vector2

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
