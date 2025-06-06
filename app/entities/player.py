import pygame

from typing import TYPE_CHECKING, Any
from enum import Enum, auto

from .entity import Entity
from ._constants import (
    PLAYER_W, PLAYER_H, ANIMATION_DELAY, PLAYER_VEL,
    PLAYER_JUMP_VEL, PLAYER_DASH_VEL, PLAYER_DASH_DURATION,
    PLAYER_DASH_COOLDOWN, PLAYER_DASH_JUMP_MULT, PLAYER_DASH_COYOTE_TIME,
    DASH_TRAIL_LENGTH, DASH_TRAIL_ALPHA, DASH_TRAIL_DELAY
)

if TYPE_CHECKING:
    from ..game import Camera


class Player(Entity):
    events: list[pygame.event.Event]
    debug: bool

    def __init__(
        self,
        name: str,
        pos: pygame.Vector2,
        *groups: 'Camera',
        editor_mode: bool = False
    ):
        super().__init__(*groups)

        super().init_moving(
            f'assets/sprites/characters/{name}',
            pos,
            PLAYER_W,
            PLAYER_H,
            scale=2,
            direction=True
        )

        self.vel = pygame.Vector2(0, 0)
        self.collide_left = False
        self.collide_right = False

        self.direction = 'right'
        self.animation_state = PlayerAnimation.IDLE
        self.animation_count = 0
        self.jump_count = 0
        self.fall_count = 0
        self.editor_mode = editor_mode
        self.debug = False
        self.is_dashing = False
        self.dash_count = 0
        self.dash_cooldown = 0
        self.dash_coyote_count = 0

        self.trail_positions: list[tuple[pygame.Rect, pygame.Surface]] = []
        self.trail_images: list[pygame.Surface] = []
        self.trail_counter = 0

        if len(groups) > 0 and isinstance(groups[0], pygame.sprite.LayeredUpdates):
            groups[0].change_layer(self, 1)

    def update(self, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

        if self.editor_mode:
            self._show_static()
            return

        if self.debug:
            super().debug_hitboxes()

        self._animate()
        self._handle_input()
        self._handle_dash_state()
        super().apply_movement()
        super().check_collisions(PLAYER_VEL)
        super().constrain_to_level()

    def _handle_input(self) -> None:
        keys = pygame.key.get_pressed()
        self.vel.x = 0

        can_dash_move = self.is_dashing or self.dash_coyote_count > 0
        current_vel = PLAYER_DASH_VEL if can_dash_move else PLAYER_VEL

        if keys[pygame.K_a] and not self.collide_left:
            super().move_horizontal(-current_vel)
        if keys[pygame.K_d] and not self.collide_right:
            super().move_horizontal(current_vel)

        for e in self.events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    self._jump(boost_enabled=can_dash_move)
                elif e.key == pygame.K_j and self.dash_cooldown <= 0:
                    self._start_dash()

    def _jump(
        self,
        boost_enabled: bool = False
    ) -> None:
        if self.jump_count >= len(PLAYER_JUMP_VEL):
            return
        base_jump_vel = PLAYER_JUMP_VEL[self.jump_count]

        jump_vel = base_jump_vel * PLAYER_DASH_JUMP_MULT if boost_enabled else base_jump_vel

        self.vel.y = jump_vel
        self.fall_count = 0
        self.jump_count += 1
        self.animation_count = 0

    def _handle_dash_state(self) -> None:
        if self.is_dashing:
            self.dash_count += 1
            if self.dash_count >= PLAYER_DASH_DURATION:
                self._end_dash()

        if self.dash_coyote_count > 0:
            self.dash_coyote_count -= 1

        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1

    def _start_dash(self) -> None:
        self.is_dashing = True
        self.dash_count = 0
        self.dash_coyote_count = 0
        self.animation_count = 0
        self.dash_cooldown = PLAYER_DASH_COOLDOWN

        # if abs(self.vel.y) > 0:  # Only apply dash for upward movement
        self.vel.y *= PLAYER_DASH_JUMP_MULT

    def _end_dash(self) -> None:
        self.is_dashing = False
        self.dash_count = 0
        self.dash_coyote_count = PLAYER_DASH_COYOTE_TIME

    def _get_animation_state(self) -> 'PlayerAnimation':
        if self.vel.y < 0:
            return PlayerAnimation.DOUBLE_JUMP if self.jump_count == 2 else PlayerAnimation.JUMP
        if self.vel.y > 2:
            return PlayerAnimation.FALL
        if self.vel.x != 0:
            return PlayerAnimation.RUN
        return PlayerAnimation.IDLE

    def _animate(self) -> None:
        self.animation_state = self._get_animation_state()
        sheet_name = f"{self.animation_state.name.lower()}_{self.direction}"
        sprites = self.sheet[sheet_name]

        max_animation_count = int(len(sprites) * ANIMATION_DELAY)
        sprite_index = int((self.animation_count // ANIMATION_DELAY) % len(sprites))

        self.animation_count = (self.animation_count + 1) % max_animation_count
        self.image = sprites[sprite_index]

        self._draw_trail()
        super().draw()
        self._update_trail()

    def _show_static(self) -> None:
        sheet_name = f"idle_{self.direction}"
        sprite = self.sheet[sheet_name][0]
        self.image = sprite
        self.mask = pygame.mask.from_surface(self.image)
        super().draw()

    def create_v_collision(self) -> tuple[pygame.Rect, pygame.Rect]:
        return super().create_v_collision_rects(
            top_offset=8,
            bottom_offset=2,
            x_offset=14
        )

    def _update_trail(self) -> None:
        """
        Updates the player's dash trail
        """
        self.trail_counter = (self.trail_counter + 1) % DASH_TRAIL_DELAY

        if self.trail_counter == 0:
            if self.is_dashing:
                self.trail_positions.append((self.rect.copy(), self.image.copy()))
                if len(self.trail_positions) > DASH_TRAIL_LENGTH:
                    self.trail_positions.pop(0)
            else:
                self.trail_positions.clear()

    def _draw_trail(self) -> None:
        """
        Draws the player's dash trail
        """
        for rect, image in self.trail_positions:
            ghost = image.copy()
            ghost.set_alpha(DASH_TRAIL_ALPHA)
            self.display.blit(
                ghost,
                (
                    rect.x - self.offset.x - self.top_left.x,
                    rect.y - self.offset.y - self.top_left.y
                )
            )


class PlayerAnimation(Enum):
    IDLE = auto()
    JUMP = auto()
    DOUBLE_JUMP = auto()
    RUN = auto()
    FALL = auto()
