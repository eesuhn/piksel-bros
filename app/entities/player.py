from typing import TYPE_CHECKING

from .entity import Entity

if TYPE_CHECKING:
    from ..game import Camera


class Player(Entity):
    def __init__(self, *groups: 'Camera'):
        super().__init__(*groups)
