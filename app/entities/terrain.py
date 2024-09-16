import pygame

from typing import TYPE_CHECKING, Any

from .entity import Entity
from ._constants import TERRAIN_W, TERRAIN_H

if TYPE_CHECKING:
    from ..game import Camera


class Terrain(Entity):
    def __init__(
        self,
        name: str,
        var: int,
        pos: pygame.Vector2,
        *groups: 'Camera'
    ):

        super().__init__(*groups)

        self.init_static_graphics(
            f'assets/images/terrains/{name}/{var}',
            pos,
            TERRAIN_W,
            TERRAIN_H
        )

        if len(groups) > 0 and isinstance(groups[0], pygame.sprite.LayeredUpdates):
            groups[0].change_layer(self, 1)

    def update(self, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

        self.draw()
