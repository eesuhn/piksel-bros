import pygame

from typing import TYPE_CHECKING

from .entity import Entity
from .._costants import RECT_W, RECT_H

if TYPE_CHECKING:
    from ..game import Camera


class Player(Entity):
    def __init__(self, name: str, pos: pygame.Vector2, *groups: 'Camera'):
        super().__init__(*groups)

        self.rect = pygame.Rect(
            pos.x * RECT_W,
            pos.y * RECT_H,
            RECT_W,
            RECT_H
        )
        print(name)
