import sys

from .game import Game
from .level_editor import Editor


class Main:
    def __init__(self) -> None:
        self.args = set(sys.argv[1:])
        self._run()

    def _run(self) -> None:
        if {'--edit', '-e'} & self.args:
            Editor().run()
        elif {'--debug', '-d'} & self.args:
            Game().run(debug=True)
        else:
            Game().run()
