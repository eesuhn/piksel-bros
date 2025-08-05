import pygame

from typing import TYPE_CHECKING, Any, Union

from ..utils import load_image
from ._constants import BG_SPEED
from .._constants import SCR_W

if TYPE_CHECKING:
    from ..game import Camera


class Background(pygame.sprite.Sprite):
    display: pygame.Surface
    bg_images: list[pygame.Surface]
    bg_speeds: list[float]
    full_bgs: list[pygame.Surface]
    target: Union[pygame.sprite.Sprite, None]
    offset: pygame.Vector2

    def __init__(self, *groups: "Camera"):
        super().__init__(*groups)
        self.target = None

        self.bg_images = []
        self.bg_speeds = []
        self.full_bgs = []
        self.map_width = 0

        if len(groups) > 0 and isinstance(groups[0], pygame.sprite.LayeredUpdates):
            self.map_width = int(groups[0].width)
            groups[0].change_layer(self, 0)

        self._load_bgs()

    def add_target(self, target: pygame.sprite.Sprite) -> None:
        self.target = target

    def _load_bgs(self) -> None:
        """
        Load the background images and speeds for each layer
        """
        for i in range(1, 6):
            bg_image = load_image(f"assets/images/background/plx-{i}")
            self.bg_images.append(bg_image)
            speed_factor = 0.6 if i == 1 else (0.4 if i <= 3 else 0.2)
            self.bg_speeds.append(int(i * BG_SPEED * speed_factor))
        self.scrolls = [0] * len(self.bg_images)
        self.bg_width = self.bg_images[0].get_width()

        # Pre-render the full background for each layer
        for image in self.bg_images:
            full_bg = pygame.Surface(
                (self.bg_width * 2, image.get_height()), pygame.SRCALPHA
            )
            for x in range(2):
                full_bg.blit(image, (x * self.bg_width, 0))
            self.full_bgs.append(full_bg)

    def update(self, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

        self._draw_bgs()
        self._scroll()

    def _draw_bgs(self) -> None:
        display_rect = self.display.get_rect()

        for i, full_bg in enumerate(self.full_bgs):
            # Blit source rect to destination for better performance
            scroll = self.scrolls[i]
            source_rect = pygame.Rect(
                scroll, 0, display_rect.width, display_rect.height
            )
            self.display.blit(full_bg, (0, 0), source_rect)

    def _scroll(self) -> None:
        if not self.target:
            return

        max_scroll = max(0, self.map_width - SCR_W)

        for i in range(len(self.scrolls)):
            parallax_factor = (i + 1) / len(self.scrolls)
            max_layer_scroll = max_scroll * parallax_factor
            new_scroll = self.offset.x * parallax_factor

            # Clamp and wrap
            new_scroll = max(0, min(new_scroll, max_layer_scroll))
            self.scrolls[i] = int(new_scroll) % self.bg_width
