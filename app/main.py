from typing import Any

from .game import Game
from .level_editor import Editor


class Main:
    def __init__(self, *argv: Any) -> None:
        if '--edit' in argv[1:] or '-e' in argv[1:]:
            Editor().run()

        elif '--debug' in argv[1:] or '-d' in argv[1:]:
            Game().run(debug=True)

        else:
            Game().run()
