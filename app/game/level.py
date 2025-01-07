import pygame
import json

from typing import TYPE_CHECKING, Union

from ..utils import load_json
from .camera import Camera
from ..entities import Entity, Terrain, Fruit, Player
from .._constants import RECT_W, RECT_H

if TYPE_CHECKING:
    from ..level_editor import EditorCamera


class Level:
    def __init__(self, level: str):
        self.level = level
        self.objs: list[Entity] = []

        data = load_json(f'levels/{level}')
        self.player = data['player']
        self.terrain = data['terrain']
        self.fruit = data['fruit']

        self.obj_dict = {
            'terrain': self.terrain,
            'fruit': self.fruit
        }

    def load(
        self,
        camera: Camera,
        target: Union['Player', 'EditorCamera']
    ) -> list[Entity]:

        self.camera = camera
        camera.add_target(target)

        self.is_editor = target.__class__.__name__ == 'EditorCamera'
        self.load_objs()
        return self.objs

    def load_objs(self) -> None:
        # Clear old objects from the camera
        self.camera.remove(*self.objs)
        self.objs.clear()

        for dic in [self.terrain, self.fruit]:
            for _, v in dic.items():
                if 'var' in v:
                    self.objs.append(
                        Terrain(
                            v['name'],
                            v['var'],
                            pygame.Vector2(v['pos']),
                            self.camera))
                else:
                    self.objs.append(
                        Fruit(
                            v['name'],
                            pygame.Vector2(v['pos']),
                            self.camera,
                            editor_mode=self.is_editor))

        if self.is_editor:
            p = Player(
                self.player['name'],
                pygame.Vector2(self.player['pos']),
                self.camera,
                editor_mode=True)
            self.objs.append(p)

        self.camera.add(*self.objs)

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

    def check_obj_dict(
        self,
        x: int,
        y: int
    ) -> str | None:

        key = f'{x};{y}'
        for k, v in self.obj_dict.items():
            if key in v:
                return k
        return None

    def is_blocked(self, x: int, y: int) -> bool:
        return self.check_obj_dict(x, y) is not None

    def add_block(
        self,
        x: int,
        y: int,
        block_type: str,
        name: str | None = None,
        variant: int | None = None
    ) -> None:

        if self.is_blocked(x, y):
            return

        if block_type == 'terrain':
            self.terrain[f'{x};{y}'] = {
                'name': name or 'stone',
                'pos': [x, y],
                'var': variant or 1
            }
        elif block_type == 'fruit':
            self.fruit[f'{x};{y}'] = {
                'name': name or 'pineapple',
                'pos': [x, y]
            }
        else:
            raise ValueError(f'Invalid block type: {block_type}')

        self.load_objs()

    def remove_block(self, x: int, y: int) -> None:
        key = f'{x};{y}'
        if key in self.terrain:
            del self.terrain[key]
        elif key in self.fruit:
            del self.fruit[key]
        self.load_objs()

    def save_level(self) -> None:
        data = {
            'player': self.player,
            'terrain': self.terrain,
            'fruit': self.fruit
        }
        with open(f'app/levels/{self.level}.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
