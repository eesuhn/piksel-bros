import pygame

from .._constants import SCR_W, SCR_H, CAM_SCALE, RECT_W, RECT_H
from ..game import Game, Level, Camera
from .editor_camera import EditorCamera
from .editor_util import EditorUtil
from ..utils import load_sprites_sheet, load_image, get_terrain_types, get_fruit_types
from ..entities._constants import FRUIT_W, FRUIT_H
from ..game._constants import SCR_FLAGS


class Editor(Game):
    def __init__(self) -> None:
        super().__init__()
        pygame.display.set_caption("Editor - Piksel Bros.")
        self.display = pygame.Surface((
            SCR_W * CAM_SCALE,
            SCR_H * CAM_SCALE
        )).convert_alpha()

        self.o_screen = pygame.Vector2((self.screen.get_size()))
        self.editor_util = EditorUtil(self)

        self.terrain_types = get_terrain_types()
        self.fruit_types = get_fruit_types()

        self.current_terrain = next(iter(self.terrain_types.keys()))
        self.current_terrain_var = self.terrain_types[self.current_terrain][0]
        self.current_fruit = self.fruit_types[0]

        self._load_previews()

    def _load_previews(self) -> None:
        # Calculate preview scale based on window height
        self.preview_scale = self.screen.get_height() / SCR_H * 0.8

        self.preview_terrain = load_image(
            f'assets/images/terrains/{self.current_terrain}/{self.current_terrain_var}',
            scale=self.preview_scale
        )

        fruit_sheet = load_sprites_sheet(
            'assets/sprites/fruits',
            FRUIT_W,
            FRUIT_H,
            scale=(2 * self.preview_scale)
        )
        self.preview_fruit = fruit_sheet[self.current_fruit][0]

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
        self._show_preview()

        pygame.display.update()

    def check_events(self) -> None:
        super().check_events()

        for event in self.events:
            if event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode(
                    (event.w, event.h),
                    SCR_FLAGS
                )
                self.o_screen = pygame.Vector2((event.w, event.h))
                self._load_previews()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.editor_util.handle_mousedown(event)

            if event.type == pygame.MOUSEBUTTONUP:
                self.editor_util.handle_mouseup(event)

            if event.type == pygame.MOUSEWHEEL:
                self._select_block(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.level.save_level()
                    # TODO: Handle message
                    print("Level saved!")

    def _select_block(self, event: pygame.event.Event) -> None:
        """
        Scroll through blocks with mouse wheel
        Hold shift to switch between block types
        """
        shift_pressed = bool(pygame.key.get_mods() & pygame.KMOD_SHIFT)

        if shift_pressed:
            self.editor_util.handle_mousewheel()

        else:
            # TODO: Refactor block type to enum
            if self.editor_util.block_type == 'terrain':
                terrains = list(self.terrain_types.keys())
                current_idx = terrains.index(self.current_terrain)
                new_idx = (current_idx + event.y) % len(terrains)
                self.current_terrain = terrains[new_idx]
                self.current_terrain_var = self.terrain_types[self.current_terrain][0]
            elif self.editor_util.block_type == 'fruit':
                current_idx = self.fruit_types.index(self.current_fruit)
                new_idx = (current_idx + event.y) % len(self.fruit_types)
                self.current_fruit = self.fruit_types[new_idx]
            else:
                raise ValueError(f'Invalid block type: {self.editor_util.block_type}')
            self._load_previews()

    def _show_preview(self) -> None:
        """
        Show preview of currently selected block in the bottom right corner
        """
        # TODO: Refactor block type to enum
        if self.editor_util.block_type == 'terrain':
            preview = self.preview_terrain
        elif self.editor_util.block_type == 'fruit':
            preview = self.preview_fruit
        else:
            raise ValueError(f'Invalid block type: {self.editor_util.block_type}')
        preview_copy = preview.copy()
        preview_copy.set_alpha(128)

        preview_x = self.screen.get_width() - int(74 * self.preview_scale)
        preview_y = self.screen.get_height() - int(74 * self.preview_scale)
        self.screen.blit(preview_copy, (preview_x, preview_y))
