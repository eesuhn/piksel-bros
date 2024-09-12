import pygame
import sys

from ._costants import SCR_W, SCR_H, FPS
from .game import Level


class Main:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Piksel Bros.")

        screen_flags = pygame.DOUBLEBUF | pygame.HWSURFACE
        self.screen = pygame.display.set_mode((SCR_W, SCR_H), screen_flags)
        self.display = pygame.Surface((SCR_W, SCR_H)).convert_alpha()
        Level("01")

    def run(self) -> None:
        self.clock = pygame.time.Clock()

        while True:
            self.check_events()
            self.loop()
            self.clock.tick(FPS)

    def check_events(self) -> None:
        self.events = pygame.event.get()

        for event in self.events:
            if event.type == pygame.QUIT:
                self.end()
            if event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)

    def handle_keydown(self, key: int) -> None:
        if key == pygame.K_ESCAPE:
            self.end()

    def end(self) -> None:
        pygame.quit()
        sys.exit()

    def loop(self) -> None:
        self.display.fill((0, 0, 0))
        self.screen.blit(
            pygame.transform.scale(self.display, self.screen.get_size()),
            (0, 0)
        )
        pygame.display.update()
