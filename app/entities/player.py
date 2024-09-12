import pygame

from .entity import Entity


class Player(Entity):
    def __init__(self, *groups: pygame.sprite.Group):
        super().__init__(*groups)
