import pygame

from typing import Any


class Camera(pygame.sprite.LayeredUpdates):
    def __init__(self, width: int = 0, height: int = 0) -> None:
        super().__init__()
        self.width = width
        self.height = height

    def add_target(self, target: Any) -> None:
        self.target = target
