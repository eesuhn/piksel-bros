import sys

from .game import Game
from .editor import Editor


class App:
	def __init__(self) -> None:
		pass

	def launch(self) -> None:
		app = self._select_app()
		app.run()

	def _select_app(self) -> object:
		if "--editor" in sys.argv or "-e" in sys.argv:
			return Editor()
		else:
			return Game()
