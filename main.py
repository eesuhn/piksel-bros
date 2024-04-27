import sys

from app import Game, Editor


def main() -> None:
	if "--editor" in sys.argv or "-e" in sys.argv:
		app = Editor()
	else:
		app = Game()
	app.run()


if __name__ == "__main__":
	main()
