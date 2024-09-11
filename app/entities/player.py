from . import Entity


class Player(Entity):
    def __init__(self, *groups):
        super().__init__(*groups)
