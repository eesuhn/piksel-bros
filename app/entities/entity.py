import pygame

from typing import TYPE_CHECKING, Callable, Union
from pathlib import Path

from ..utils import load_sprites_sheet, load_image
from ._constants import MAX_GRAVITY, GRAVITY_ACC, GRAVITY_FRAME

if TYPE_CHECKING:
    from ..game import Camera
    from .player import Player


class Entity(pygame.sprite.Sprite):
    image: pygame.Surface
    rect: pygame.Rect
    display: pygame.Surface
    offset: pygame.Vector2
    top_left: pygame.Vector2
    bottom_right: pygame.Vector2

    objs: list['Entity']
    vel: pygame.Vector2
    fall_count: int

    # TODO: I don't think this is a good practice, but whatever it works
    # Child callable to include `create_v_collision_rects`
    create_v_collision: Callable

    def __init__(self, *groups: 'Camera'):
        super().__init__(*groups)
        self.pass_through = False
        self.collectable = False

    def draw(self) -> None:
        self.display.blit(
            self.image,
            (
                self.rect.x - self.offset.x - self.top_left.x,
                self.rect.y - self.offset.y - self.top_left.y
            )
        )

    def init_moving(
        self,
        relative_path: Union[str, Path],
        pos: pygame.Vector2,
        width: int,
        height: int,
        scale: int = 1,
        direction: bool = False
    ) -> None:
        """
        Initialize moving graphics and hitboxes for the entity.
        """

        scaled_width = width * scale
        scaled_height = height * scale

        self.rect = pygame.Rect(
            pos.x * scaled_width,
            pos.y * scaled_height,
            scaled_width,
            scaled_height
        )
        self.sheet = load_sprites_sheet(
            relative_path,
            width,
            height,
            scale=scale,
            direction=direction
        )
        self.image = pygame.Surface(
            (scaled_width, scaled_height)
        ).convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.head_rect, self.feet_rect = self.create_v_collision()

    def init_static(
        self,
        relative_path: Union[str, Path],
        pos: pygame.Vector2,
        width: int,
        height: int,
        scale: int = 1
    ) -> None:
        """
        Initialize static graphics and hitboxes for the entity.
        """

        scaled_width = width * scale
        scaled_height = height * scale

        self.rect = pygame.Rect(
            pos.x * scaled_width,
            pos.y * scaled_height,
            scaled_width,
            scaled_height
        )
        self.image = load_image(relative_path)
        self.mask = pygame.mask.from_surface(self.image)

    def create_v_collision_rects(
        self,
        top_offset: int,
        bottom_offset: int,
        x_offset: int = 0
    ) -> tuple[pygame.Rect, pygame.Rect]:
        """
        Create vertical collision rects.
        """

        def create_rect(
            x_offset: Union[float, int],
            y_offset: Union[float, int]
        ) -> pygame.Rect:
            width = self.rect.width - (x_offset * 2)
            height = 2
            return pygame.Rect(
                self.rect.x + x_offset,
                self.rect.y + y_offset,
                width,
                height
            )

        top_rect = create_rect(x_offset, top_offset)
        bottom_rect = create_rect(
            x_offset,
            self.rect.height - bottom_offset
        )

        return top_rect, bottom_rect

    def move_horizontal(self, speed: int = 1) -> None:
        self.vel.x = speed
        self.direction = 'right' if speed > 0 else 'left'

    def apply_movement(self) -> None:
        self.rect.move_ip(self.vel.x, self.vel.y)
        self._update_hitboxes()

    def _update_hitboxes(self) -> None:
        self.mask = pygame.mask.from_surface(self.image)
        self.head_rect, self.feet_rect = self.create_v_collision()

    def constrain_to_level(self) -> None:
        """
        Constrain the entity to the level bounds.
        """
        self.rect.left = max(self.rect.left, int(self.top_left.x))
        self.rect.right = min(self.rect.right, int(self.bottom_right.x))

    def _apply_gravity(self) -> None:
        factor = min(GRAVITY_ACC, self.fall_count / GRAVITY_FRAME)
        self.vel.y += factor

        if self.fall_count < GRAVITY_FRAME:
            self.fall_count += 1

        self.vel.y = min(self.vel.y, MAX_GRAVITY)

    def check_collisions(self, entity_vel: int) -> None:
        """
        Check both horizontal and vertical collisions.
        """
        self._check_v_collision()
        dx_check = entity_vel * 1.2
        self.collide_left = self._check_h_collision(-dx_check)
        self.collide_right = self._check_h_collision(dx_check)
        self._apply_gravity()

    def _check_v_collision(self) -> None:
        """
        Check vertical collision based on entity's head and feet.
        """
        for obj in [o for o in self.objs if not o.pass_through]:
            if self.head_rect.colliderect(obj.rect):
                self.rect.top = obj.rect.bottom
                self._hit_head()
                break
            if self.feet_rect.colliderect(obj.rect):
                self.rect.bottom = obj.rect.top
                self._land()
                break

    def _hit_head(self) -> None:
        self.vel.y = 0

    def _land(self) -> None:
        self.fall_count = 0
        self.jump_count = 0
        self.vel.y = 0

    def _check_h_collision(self, dx: float) -> bool:
        original_x = self.rect.x
        self.rect.x += int(dx)
        collided = any(
            pygame.sprite.collide_mask(self, obj)
            for obj in [o for o in self.objs if not o.pass_through]
        )
        self.rect.x = original_x
        return collided

    def debug_hitboxes(self) -> None:
        """
        Draw hitboxes for debugging.
        """
        def draw_rect(rect: pygame.Rect, color: tuple[int, int, int]) -> None:
            pygame.draw.rect(
                self.display,
                color,
                rect.move(
                    -self.offset.x - self.top_left.x,
                    -self.offset.y - self.top_left.y
                )
            )

        draw_rect(self.rect, (0, 255, 0))
        draw_rect(self.head_rect, (255, 0, 0))
        draw_rect(self.feet_rect, (255, 0, 0))

    def check_collected(self, player: 'Player') -> bool:
        """
        To be implemented by collectable child classes.
        """
        del player
        return False
