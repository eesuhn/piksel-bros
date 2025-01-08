import pygame

from typing import Any

from .._constants import SCR_W, SCR_H
from ._constants import OFFSET_DELAY


class Camera(pygame.sprite.LayeredUpdates):
    def __init__(self, width: float = 0, height: float = 0) -> None:
        super().__init__()
        self.width = width
        self.height = height
        self.offset = pygame.Vector2(0, 0)
        self.top_left = pygame.Vector2(0, 0)
        self.set_border = False
        self.camera_delay = False

    def add_target(self, target: Any) -> None:
        self.target = target

    def update(self, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

        self.calculate_offset()

        super().update(offset=self.offset, **kwargs)

    def calculate_offset(self) -> None:
        """
        Calculate the offset of the camera based on the target position and screen center.
        """
        target_pos = pygame.Vector2(self.target.rect.centerx, self.target.rect.centery)
        screen_center = pygame.Vector2(SCR_W // 2, SCR_H // 2)
        desired_offset = target_pos - screen_center - self.top_left

        if self.camera_delay:
            self.offset += (desired_offset - self.offset) / OFFSET_DELAY
        else:
            self.offset = desired_offset

        # Clamp the offset to the borders of the level, not vertically
        if self.set_border:
            self.offset.x = max(0, min(self.offset.x, self.width - SCR_W))
            self.offset.y = min(self.offset.y, self.height - SCR_H)
