import sys

from .game import Game
from .editor import Editor


class App:
	def select_app() -> object:
		if "--editor" in sys.argv or "-e" in sys.argv:
			return Editor()
		else:
			return Game()
