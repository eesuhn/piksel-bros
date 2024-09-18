import sys

from .game import Game
from .level_editor import Editor


class Main:
    def __init__(self) -> None:
        if '--editor' in sys.argv or '-e' in sys.argv:
            Editor().run()
        else:
            Game().run()
