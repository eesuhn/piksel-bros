import pygame

from ._costants import SCR_W, SCR_H, FPS


class Main:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Piksel Bros.")

        screen_flags = pygame.DOUBLEBUF | pygame.HWSURFACE
        self.screen = pygame.display.set_mode((SCR_W, SCR_H), screen_flags)
        self.display = pygame.Surface((SCR_W, SCR_H)).convert_alpha()

    def run(self) -> None:
        self.clock = pygame.time.Clock()

        while True:
            self.loop()
            self.clock.tick(FPS)

    def loop(self) -> None:
        self.display.fill((0, 0, 0))
        self.screen.blit(
            pygame.transform.scale(self.display, self.screen.get_size()),
            (0, 0)
        )
        pygame.display.update()
