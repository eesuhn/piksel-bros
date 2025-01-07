import sys

from .game import Game
from .level_editor import Editor


class Main:
    def __init__(self) -> None:
        if '--editor' in sys.argv or '-e' in sys.argv:
            Editor().run()
        elif '--debug' in sys.argv or '-d' in sys.argv:
            Game().run(debug=True)
        else:
            Game().run()
