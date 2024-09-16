import pygame

from typing import TYPE_CHECKING, Any

from .entity import Entity
from .._costants import RECT_W, RECT_H
from ..utils import load_image

if TYPE_CHECKING:
    from ..game import Camera


class Terrain(Entity):
    def __init__(
        self,
        name: str,
        var: int,
        pos: list[int, int],
        *groups: 'Camera'
    ):

        super().__init__(*groups)
        self.rect = pygame.Rect(
            pos[0] * RECT_W,
            pos[1] * RECT_H,
            RECT_W,
            RECT_H
        )
        self.image = load_image(f'assets/images/terrains/{name}/{var}')
        self.mask = pygame.mask.from_surface(self.image)

        if len(groups) > 0 and isinstance(groups[0], pygame.sprite.LayeredUpdates):
            groups[0].change_layer(self, 1)

    def update(self, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

        self.draw()
