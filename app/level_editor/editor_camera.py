import pygame

from typing import TYPE_CHECKING, Any

from .._constants import SCR_W, SCR_H, CAM_SCALE
from ._constants import CAM_VEL

if TYPE_CHECKING:
    from ..game import Camera


class EditorCamera(pygame.sprite.Sprite):
    image: pygame.Surface
    display: pygame.Surface

    def __init__(
        self,
        x: int,
        y: int,
        *groups: 'Camera'
    ):
        super().__init__(*groups)
        self.rect = pygame.Rect(x, y, SCR_W, SCR_H)
        self.image = pygame.Surface((
            SCR_W * CAM_SCALE,
            SCR_H * CAM_SCALE
        )).convert_alpha()
        self.scroll = pygame.Vector2((x, y))

        if len(groups) > 0 and isinstance(groups[0], pygame.sprite.LayeredUpdates):
            groups[0].change_layer(self, 2)

    def update(self, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

        self.draw()
        self.move()

    def draw(self) -> None:
        self.image.fill((0, 0, 0, 0))
        self.display.blit(self.image, (0, 0))

    def move(self) -> None:
        keys = pygame.key.get_pressed()
        x_dir = (keys[pygame.K_d] - keys[pygame.K_a]) * CAM_VEL
        y_dir = (keys[pygame.K_s] - keys[pygame.K_w]) * CAM_VEL

        # Normalize diagonal movement
        if x_dir and y_dir:
            x_dir = int(x_dir * 0.7071)
            y_dir = int(y_dir * 0.7071)

        self.rect.x += x_dir
        self.rect.y += y_dir
        self.scroll.x += x_dir
        self.scroll.y += y_dir

        self.set_editor_border()

    def set_editor_border(self) -> None:
        self.rect.x = max(0, self.rect.x)
        self.rect.y = max(0, self.rect.y)
        self.scroll.x = max(0, self.scroll.x)
        self.scroll.y = max(0, self.scroll.y)
