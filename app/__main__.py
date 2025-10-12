import argparse

from .game import Game
from .level_editor import Editor
from typing import Callable


class Main:
    def __init__(self) -> None:
        self.parse_args()
        self.parse_options()

    def parse_args(self) -> None:
        args_parser = argparse.ArgumentParser(description="Piksel Bros.")
        args_parser.add_argument(
            dest="options",
            type=str,
            nargs="?",
            choices=["edit", "debug", "multiplayer"],
            help="Option to run",
            default=None,
        )
        args_parser.add_argument(
            "--name",
            type=str,
            default="Player",
            help="Player name for multiplayer mode",
        )
        args_parser.add_argument(
            "--server",
            type=str,
            default="ws://localhost:8765",
            help="Server URL for multiplayer mode",
        )
        self.args = args_parser.parse_args()

    def parse_options(self) -> None:
        game = Game()
        editor = Editor()

        option_handlers: dict[str, Callable[[], None]] = {
            "edit": lambda: editor.run(),
            "debug": lambda: game.run(debug=True),
            "multiplayer": lambda: Game(
                multiplayer=True, player_name=self.args.name
            ).run(),
        }

        if self.args.options and self.args.options in option_handlers:
            option_handlers[self.args.options]()
        else:
            game.run()
