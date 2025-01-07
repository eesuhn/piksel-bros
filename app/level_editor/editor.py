import pygame

from .._constants import SCR_W, SCR_H, CAM_SCALE, RECT_W, RECT_H
from ..game import Game, Level, Camera
from .editor_camera import EditorCamera
from .editor_util import EditorUtil
from ..utils import load_sprites_sheet, load_image


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

        self.preview_terrain = load_image('assets/images/terrains/stone/1')

        fruit_sheet = load_sprites_sheet('assets/sprites/fruits', 32, 32)
        self.preview_fruit = fruit_sheet['pineapple'][0]

        self.preview_terrain = pygame.transform.scale(self.preview_terrain, (64, 64))
        self.preview_fruit = pygame.transform.scale(self.preview_fruit, (64, 64))

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
            level=self.level,
            wpos=self.editor_camera.mpos_to_wpos(self.o_screen),
            o_screen=self.o_screen,
            player_pos=self.player_pos
        )
        self.editor_util.check_mouse()

        self.screen.blit(
            pygame.transform.scale(self.display, self.screen.get_size()),
            (0, 0)
        )

        # Show preview of current block type
        preview = self.preview_terrain if self.editor_util.block_type == 'terrain' else self.preview_fruit
        preview_copy = preview.copy()
        preview_copy.set_alpha(128)

        # Position in bottom-left corner with padding
        preview_x = 10
        preview_y = self.screen.get_height() - 74
        self.screen.blit(preview_copy, (preview_x, preview_y))

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

            if event.type == pygame.MOUSEWHEEL:
                shift_pressed = bool(pygame.key.get_mods() & pygame.KMOD_SHIFT)
                self.editor_util.handle_mousewheel(event, shift_pressed)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.level.save_level()
                    print("Level saved!")

    def handle_mousedown(self, event: pygame.event.Event) -> None:
        self.editor_util.handle_mousedown(event)

    def handle_mouseup(self, event: pygame.event.Event) -> None:
        self.editor_util.handle_mouseup(event)
