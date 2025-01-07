import pygame

from typing import Any


class EditorUtil:
    event: pygame.event.Event
    wpos: pygame.Vector2
    player_pos: pygame.Vector2

    def __init__(self) -> None:
        self.left_click = False
        self.right_click = False

    def update(self, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    def handle_mousedown(self, event: pygame.event.Event) -> None:
        if event.button == 1:
            if not self.right_click:
                self.left_click = True
        if event.button == 3:
            if not self.left_click:
                self.right_click = True

    def handle_mouseup(self, event: pygame.event.Event) -> None:
        if event.button == 1:
            self.left_click = False
        if event.button == 3:
            self.right_click = False

    def mpos_is_player(self) -> bool:
        return self.wpos.x == self.player_pos.x and self.wpos.y == self.player_pos.y

    def check_mouse(self) -> None:
        x, y = int(self.wpos.x), int(self.wpos.y)

        if self.left_click:
            if not self.mpos_is_player():
                # TODO: Add block
                print(f'Adding block at {x}, {y}')

        if self.right_click:
            # TODO: Remove block
            print(f'Removing block at {x}, {y}')
