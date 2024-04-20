import sys

from app import Game, Editor


def main() -> None:
	if "-e" in sys.argv:
		app = Editor()
	else:
		app = Game()
	app.run()


if __name__ == "__main__":
	main()
