import pygame

from typing import TYPE_CHECKING, Union

from ..utils import load_json
from .camera import Camera
from ..entities import Entity, Terrain, Fruit
from .._constants import RECT_W, RECT_H

if TYPE_CHECKING:
    from ..entities import Player
    from ..level_editor import EditorCamera


class Level:
    def __init__(self, level: str):
        self.level = level
        self.objs: list[Entity] = []

        data = load_json(f'levels/{level}')
        self.player = data['player']
        self.background = data['background']
        self.terrain = data['terrain']
        self.fruit = data['fruit']

    def load(
        self,
        camera: Camera,
        target: Union['Player', 'EditorCamera']
    ) -> list[Entity]:

        self.camera = camera
        camera.add_target(target)

        self.load_terrain()
        self.load_fruit()
        return self.objs

    def load_terrain(self) -> None:
        for _, v in self.terrain.items():
            self.objs.append(
                Terrain(
                    v['name'],
                    v['var'],
                    pygame.Vector2(v['pos']),
                    self.camera
                )
            )

    def load_fruit(self) -> None:
        for _, v in self.fruit.items():
            self.objs.append(
                Fruit(
                    v['name'],
                    pygame.Vector2(v['pos']),
                    self.camera
                )
            )

    def get_top_left(self) -> pygame.Vector2:
        """
        Returns (top, left) coordinate of the level.
        """
        min_x = min_y = float('inf')

        for _, v in self.terrain.items():
            min_x = min(min_x, v['pos'][0])
            min_y = min(min_y, v['pos'][1])

        return pygame.Vector2(
            min_x * RECT_W,
            min_y * RECT_H
        )

    def get_bottom_right(self) -> pygame.Vector2:
        """
        Returns (bottom, right) coordinate of the level.
        """
        max_x = max_y = 0

        for _, v in self.terrain.items():
            max_x = max(max_x, v['pos'][0])
            max_y = max(max_y, v['pos'][1])

        return pygame.Vector2(
            (max_x + 1) * RECT_W,
            (max_y + 1) * RECT_H
        )

    def get_dimensions(self) -> tuple[float, float]:
        return (
            self.get_bottom_right().x - self.get_top_left().x,
            self.get_bottom_right().y - self.get_top_left().y
        )

    def get_player_pos(self) -> pygame.Vector2:
        return pygame.Vector2(
            self.player['pos'][0],
            self.player['pos'][1]
        )

    def get_player_name(self) -> str:
        return self.player['name']
