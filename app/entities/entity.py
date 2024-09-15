import pygame

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..game import Camera


class Entity(pygame.sprite.Sprite):
    def __init__(self, *groups: 'Camera'):
        super().__init__(*groups)
