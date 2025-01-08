import pygame

from typing import Any

from .._constants import SCR_W, SCR_H


class Camera(pygame.sprite.LayeredUpdates):
    def __init__(self, width: float = 0, height: float = 0) -> None:
        super().__init__()
        self.width = width
        self.height = height
        self.offset = pygame.Vector2(0, 0)
        self.top_left = pygame.Vector2(0, 0)
        self.set_border = False

    def add_target(self, target: Any) -> None:
        self.target = target

    def update(self, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

        self.calculate_offset()

        super().update(offset=self.offset, **kwargs)

    def calculate_offset(self) -> None:
        x = (self.target.rect.centerx - (SCR_W // 2)) - self.top_left.x
        y = (self.target.rect.centery - (SCR_H // 2)) - self.top_left.y

        if self.set_border:
            x = max(0, min(x, self.width - SCR_W))
            y = min(y, self.height - SCR_H)

        self.offset.x = x
        self.offset.y = y
