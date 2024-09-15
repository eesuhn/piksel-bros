import pygame

from typing import Any

from .._costants import SCR_W, SCR_H


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
        """
        Args:
            `self.top_left`
        """
        x = (-SCR_W // 2) + self.target.rect.centerx - self.offset.x - self.top_left.x
        y = (-SCR_H // 2) + self.target.rect.centery - self.offset.y - self.top_left.y

        self.offset.x += x
        self.offset.y += y

        print(f"offset: {self.offset}")
