import pygame

from typing import TYPE_CHECKING

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
