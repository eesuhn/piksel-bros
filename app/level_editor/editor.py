import pygame

from .._costants import SCR_W, SCR_H, CAM_SCALE


class Editor:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Editor - Piksel Bros.")

        screen_flags = pygame.DOUBLEBUF | pygame.HWSURFACE
        self.screen = pygame.display.set_mode((SCR_W, SCR_H), screen_flags)
        self.display = pygame.Surface((
            SCR_W * CAM_SCALE,
            SCR_H * CAM_SCALE
        )).convert_alpha()

    def run(self) -> None:
        pass
