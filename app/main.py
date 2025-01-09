from typing import Any

from .game import Game
from .level_editor import Editor


class Main:
    def __init__(self, *argv: Any) -> None:
        self.args = set(argv[1:])
        self._run()

    def _run(self) -> None:
        if {'--edit', '-e'} & self.args:
            Editor().run()
        elif {'--debug', '-d'} & self.args:
            Game().run(debug=True)
        else:
            Game().run()
