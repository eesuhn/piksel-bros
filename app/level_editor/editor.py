import pygame

from .._constants import SCR_W, SCR_H, CAM_SCALE
from ..game import Game


class Editor(Game):
    def __init__(self) -> None:
        super().__init__()
        pygame.display.set_caption("Editor - Piksel Bros.")
        self.display = pygame.Surface((
            SCR_W * CAM_SCALE,
            SCR_H * CAM_SCALE
        )).convert_alpha()

    def load_level(self) -> None:
        pass
