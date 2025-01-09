import pygame

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..game import Level
    from .editor import Editor


class EditorUtil:
    event: pygame.event.Event
    wpos: pygame.Vector2
    player_pos: pygame.Vector2
    level: 'Level'
    editor: 'Editor'

    def __init__(self, editor: 'Editor') -> None:
        self.left_click = False
        self.right_click = False
        self.block_type = 'terrain'
        self.dragging_player = False
        self.player_following = False
        self.editor = editor

    def update(self, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    def _add_block(self, x: int, y: int) -> None:
        if not self._mpos_is_player():
            # TODO: Refactor block type to enum
            if self.block_type == 'terrain':
                self.level.add_block(
                    x,
                    y,
                    'terrain',
                    self.editor.current_terrain,
                    self.editor.current_terrain_var)
            elif self.block_type == 'fruit':
                self.level.add_block(
                    x,
                    y,
                    'fruit',
                    self.editor.current_fruit)
            else:
                raise ValueError(f'Invalid block type: {self.block_type}')

    def handle_mousedown(self, event: pygame.event.Event) -> None:
        if event.button == 1:
            if self.player_following:
                # Only place player if the target tile is not blocked
                x, y = int(self.wpos.x), int(self.wpos.y)
                if not self.level.is_blocked(x, y):
                    self.player_following = False  # Second click: Place the player
                    self.level.player['pos'] = [x, y]
                    self.player_pos.x, self.player_pos.y = x, y
                    self.level.load_objs()

            elif self._mpos_is_player():
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

    def handle_mousewheel(self) -> None:
        # TODO: Refactor block type to enum
        self.block_type = 'fruit' if self.block_type == 'terrain' else 'terrain'

    def _mpos_is_player(self) -> bool:
        return self.wpos.x == self.player_pos.x and self.wpos.y == self.player_pos.y

    def check_mouse(self) -> None:
        x, y = int(self.wpos.x), int(self.wpos.y)

        if self.player_following:
            # Only show player preview if the target tile is not blocked
            if not self.level.is_blocked(x, y):
                self.level.player['pos'] = [x, y]
                self.player_pos.x, self.player_pos.y = x, y
                self.level.load_objs()
            return

        if self.dragging_player:
            self.level.player['pos'] = [x, y]
            self.player_pos.x, self.player_pos.y = x, y
            return

        if self.left_click:
            self._add_block(x, y)

        if self.right_click:
            self.level.remove_block(x, y)
