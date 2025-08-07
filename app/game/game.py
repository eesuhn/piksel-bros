import pygame
import sys
import justsdk

from .._constants import SCR_W, SCR_H, FPS
from .level import Level
from .camera import Camera
from .background import Background
from ..entities import Player
from ..entities._constants import PLAYER_H
from ._constants import SCR_FLAGS


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Piksel Bros.")

        self.screen = pygame.display.set_mode((SCR_W, SCR_H), SCR_FLAGS)
        self.display = pygame.Surface((SCR_W, SCR_H)).convert_alpha()

    def run(self, debug: bool = False) -> None:
        self.debug = debug
        self.win = False
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
                self._end()
            if event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)

    def handle_keydown(self, key: int) -> None:
        if key == pygame.K_ESCAPE:
            self._end()

    def _end(self) -> None:
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
            bottom_right=self.bottom_right,
            debug=self.debug,
            set_border=True,
            camera_delay=True,
        )

        self._check_state()

        self.screen.blit(
            pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)
        )
        pygame.display.update()

    def load_level(self) -> None:
        self.level = Level("01")

        level_w, level_h = self.level.get_dimensions()
        self.top_left = self.level.get_top_left()
        self.bottom_right = self.level.get_bottom_right()

        self.camera = Camera(level_w, level_h)
        self.player = Player(
            self.level.get_player_name(), self.level.get_player_pos(), self.camera
        )
        self.objs = self.level.load(self.camera, self.player)

        # No background in debug mode
        if not self.debug:
            self.background = Background(self.camera)
            self.background.add_target(self.player)

    def _check_state(self) -> None:
        """
        Monitor the state of the game.
        """
        self._check_collectables()
        self._check_win()
        self._check_fallen()

    def _check_collectables(self) -> None:
        """
        Update and check if all collectables have been collected.
        """
        for obj in [o for o in self.objs if o.collectable]:
            if obj.check_collected(self.player):
                obj.kill()
                self.objs.remove(obj)

    def _check_win(self) -> None:
        """
        Monitor winning condition(s).
        """
        if not any(o.collectable for o in self.objs) and not self.win:
            # TODO: Handle message
            justsdk.print_info("You won!")
            self.win = True

    def _check_fallen(self) -> None:
        """
        Check if the player has fallen out of the map.
        """
        fall_limit = self.bottom_right.y + (PLAYER_H * 10)
        if self.player.rect.top > fall_limit:
            # TODO: Handle message
            justsdk.print_info("You fell out of the map!")
            self._end()
