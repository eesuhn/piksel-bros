from ..utils import load_json
from .camera import Camera
from ..entities import Player, Terrain


class Level:
    def __init__(self, level: str):
        self.level = level
        self.objs: list[Terrain] = []

        data = load_json(f'game/levels/{level}.json')
        self.player = data['player']
        self.background = data['background']
        self.terrain = data['terrain']

    def load(
        self,
        camera: Camera,
        target: Player,
        edit: bool = False
    ) -> list[Terrain]:

        self.camera = camera
        camera.add_target(target)

        if not edit:
            pass

        self.load_terrain()
        return self.objs

    def load_terrain(self) -> None:
        for _, v in self.terrain.items():
            self.objs.append(
                Terrain(
                    v['name'],
                    v['var'],
                    v['pos'][0],
                    v['pos'][1],
                    self.camera
                )
            )
