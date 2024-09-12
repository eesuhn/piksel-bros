from ..utils import load_json


class Level:
    def __init__(self, level: str):
        self.level = level

        data = load_json(f'game/levels/{level}.json')
        print(data)
