import pygame

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..game import Level


class EditorUtil:
    event: pygame.event.Event
    wpos: pygame.Vector2
    player_pos: pygame.Vector2
    level: 'Level'

    def __init__(self) -> None:
        self.left_click = False
        self.right_click = False
        self.block_type = 'terrain'
        self.dragging_player = False
        self.player_following = False

    def update(self, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    def handle_mousedown(self, event: pygame.event.Event) -> None:
        if event.button == 1:
            if self.player_following:
                self.player_following = False  # Second click: Place the player

            elif self.mpos_is_player():
                self.player_following = True  # First click: Player starts following

            elif not self.right_click:
                self.left_click = True

        if event.button == 3:
            if not self.left_click:
                self.right_click = True

    def handle_mouseup(self, event: pygame.event.Event) -> None:
        if event.button == 1:
            if self.dragging_player:
                self.dragging_player = False
            else:
                self.left_click = False
        if event.button == 3:
            self.right_click = False

    def handle_mousewheel(self, event: pygame.event.Event, shift_pressed: bool) -> None:
        del event
        if shift_pressed:
            self.block_type = 'fruit' if self.block_type == 'terrain' else 'terrain'

    def mpos_is_player(self) -> bool:
        return self.wpos.x == self.player_pos.x and self.wpos.y == self.player_pos.y

    def check_mouse(self) -> None:
        x, y = int(self.wpos.x), int(self.wpos.y)

        if self.player_following:
            self.level.player['pos'] = [x, y]
            self.player_pos.x, self.player_pos.y = x, y
            self.level.load_objs()
            return

        if self.dragging_player:
            self.level.player['pos'] = [x, y]
            self.player_pos.x, self.player_pos.y = x, y
            return

        if self.left_click:
            if not self.mpos_is_player():
                self.level.add_block(x, y, self.block_type)

        if self.right_click:
            self.level.remove_block(x, y)
