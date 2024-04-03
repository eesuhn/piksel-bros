import sys
from app.game import Game
from test import build_test


def main() -> None:
	if len(sys.argv) == 2 and sys.argv[1] == "test":
		build_test()
		return

	game = Game()
	game.run()


if __name__ == "__main__":
	main()
