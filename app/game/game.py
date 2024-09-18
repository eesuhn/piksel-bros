import pygame
import sys

from .._costants import SCR_W, SCR_H, FPS
from .level import Level
from .camera import Camera
from ..entities import Player


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Piksel Bros.")

        screen_flags = pygame.DOUBLEBUF | pygame.HWSURFACE
        self.screen = pygame.display.set_mode((SCR_W, SCR_H), screen_flags)
        self.display = pygame.Surface((SCR_W, SCR_H)).convert_alpha()

    def run(self) -> None:
        self.clock = pygame.time.Clock()
        self.load_level()

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
        """
        Main loop of the game.
        """
        self.display.fill((0, 0, 0))

        self.camera.update(
            events=self.events,
            display=self.display,
            objs=self.objs,
            top_left=self.top_left,
            bottom_right=self.bottom_right
        )

        self.screen.blit(
            pygame.transform.scale(self.display, self.screen.get_size()),
            (0, 0)
        )
        pygame.display.update()

    def load_level(self) -> None:
        self.level = Level('01')

        level_w, level_h = self.level.get_dimensions()
        self.top_left = self.level.get_top_left()
        self.bottom_right = self.level.get_bottom_right()

        self.camera = Camera(level_w, level_h)
        self.player = Player(
            self.level.get_player_name(),
            self.level.get_player_pos(),
            self.camera
        )
        self.objs = self.level.load(self.camera, self.player)
