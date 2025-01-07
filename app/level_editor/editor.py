import pygame

from .._constants import SCR_W, SCR_H, CAM_SCALE, RECT_W, RECT_H
from ..game import Game, Level, Camera
from .editor_camera import EditorCamera


class Editor(Game):
    def __init__(self) -> None:
        super().__init__()
        pygame.display.set_caption("Editor - Piksel Bros.")
        self.display = pygame.Surface((
            SCR_W * CAM_SCALE,
            SCR_H * CAM_SCALE
        )).convert_alpha()

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

        self.screen.blit(
            pygame.transform.scale(self.display, self.screen.get_size()),
            (0, 0)
        )
        pygame.display.update()
