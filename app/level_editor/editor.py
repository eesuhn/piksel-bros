import pygame

from .._constants import SCR_W, SCR_H, CAM_SCALE, RECT_W, RECT_H
from ..game import Game, Level, Camera
from .editor_camera import EditorCamera
from .editor_util import EditorUtil


class Editor(Game):
    def __init__(self) -> None:
        super().__init__()
        pygame.display.set_caption("Editor - Piksel Bros.")
        self.display = pygame.Surface((
            SCR_W * CAM_SCALE,
            SCR_H * CAM_SCALE
        )).convert_alpha()

        self.o_screen = pygame.Vector2((self.screen.get_size()))
        self.editor_util = EditorUtil()

    def load_level(self) -> None:
        self.level = Level('01')

        self.camera = Camera()
        self.player_pos = self.level.get_player_pos()

        camera_pos = pygame.Vector2((
            (self.player_pos.x * RECT_W) - (SCR_W // 2),
            (self.player_pos.y * RECT_H) - (SCR_H // 2)
        ))
        self.editor_camera = EditorCamera(
            int(camera_pos.x),
            int(camera_pos.y),
            self.camera
        )

        self.level.load(self.camera, self.editor_camera)

    def loop(self) -> None:
        self.display.fill((0, 0, 0))

        self.camera.update(
            display=self.display,
            top_left=pygame.Vector2((0, 0))
        )
        self.editor_util.update(
            wpos=self.editor_camera.mpos_to_wpos(self.o_screen),
            o_screen=self.o_screen,
            player_pos=self.player_pos
        )
        self.editor_util.check_mouse()

        self.screen.blit(
            pygame.transform.scale(self.display, self.screen.get_size()),
            (0, 0)
        )
        pygame.display.update()

    def check_events(self) -> None:
        super().check_events()

        for event in self.events:
            if event.type == pygame.VIDEORESIZE:
                self.o_screen = pygame.Vector2((event.w, event.h))
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mousedown(event)
            if event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouseup(event)

    def handle_mousedown(self, event: pygame.event.Event) -> None:
        self.editor_util.handle_mousedown(event)

    def handle_mouseup(self, event: pygame.event.Event) -> None:
        self.editor_util.handle_mouseup(event)
