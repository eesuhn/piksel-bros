from typing import TYPE_CHECKING

from .entity import Entity

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
        print(name, var, pos)
