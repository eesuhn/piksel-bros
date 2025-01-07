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

    def add_target(self, target: Any) -> None:
        self.target = target

    def update(self, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

        self.calculate_offset()

        super().update(offset=self.offset, **kwargs)

    def calculate_offset(self) -> None:
        x = (-SCR_W // 2) + self.target.rect.centerx - self.offset.x - self.top_left.x
        y = (-SCR_H // 2) + self.target.rect.centery - self.offset.y - self.top_left.y

        self.offset.x += x
        self.offset.y += y

        # TODO: Add option to clamp
        # Clamp the offset to the map size
        self.offset.x = max(0, min(self.offset.x, self.width - SCR_W))
        self.offset.y = min(self.offset.y, self.height - SCR_H)
