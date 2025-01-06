import pygame

from typing import TYPE_CHECKING, Any

from ..utils import load_image
from ._constants import BG_SPEED
from .._costants import SCR_W

if TYPE_CHECKING:
    from ..game import Camera


class Background(pygame.sprite.Sprite):
    display: pygame.Surface
    bg_images: list[pygame.Surface]
    bg_speeds: list[float]
    full_bgs: list[pygame.Surface]

    def __init__(self, *groups: 'Camera'):
        super().__init__(*groups)

        self.bg_images = []
        self.bg_speeds = []
        self.full_bgs = []
        self.map_width = 0

        if len(groups) > 0 and isinstance(groups[0], pygame.sprite.LayeredUpdates):
            self.map_width = int(groups[0].width)
            groups[0].change_layer(self, 0)

        self.load_bgs()

    def load_bgs(self) -> None:
        """
        Load the background images and speeds for each layer
            - Parallax between 1 to 3, 40% of the base speed
            - Parallax between 4 to 5, 20% of the base speed
        """
        for i in range(1, 6):
            bg_image = load_image(f'assets/images/background/plx-{i}')
            self.bg_images.append(bg_image)
            if i <= 3:
                self.bg_speeds.append(int(i * BG_SPEED * 0.4))
            else:
                self.bg_speeds.append(int(i * BG_SPEED * 0.2))
        self.scrolls = [0] * len(self.bg_images)
        self.bg_width = self.bg_images[0].get_width()

        # Pre-render the full background for each layer
        for image in self.bg_images:
            full_bg = pygame.Surface((self.bg_width * 2, image.get_height()), pygame.SRCALPHA)
            for x in range(2):
                full_bg.blit(image, (x * self.bg_width, 0))
            self.full_bgs.append(full_bg)

    def update(self, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

        self.draw_bgs()
        self.scroll()

    def draw_bgs(self) -> None:
        display_rect = self.display.get_rect()

        for i, full_bg in enumerate(self.full_bgs):
            # Blit source rect to destination for better performance
            scroll = self.scrolls[i]
            source_rect = pygame.Rect(scroll, 0, display_rect.width, display_rect.height)
            self.display.blit(full_bg, (0, 0), source_rect)

    def scroll(self) -> None:
        max_scroll = max(0, self.map_width - SCR_W)
        keys = pygame.key.get_pressed()

        for i in range(len(self.scrolls)):
            scroll_change = 0
            if keys[pygame.K_LEFT]:
                scroll_change = int(-self.bg_speeds[i])
            if keys[pygame.K_RIGHT]:
                scroll_change = int(self.bg_speeds[i])

            # Scale the scroll change based on the parallax layer
            parallax_factor = (i + 1) / len(self.scrolls)
            max_layer_scroll = max_scroll * parallax_factor

            # Update and clamp the scroll value
            new_scroll = self.scrolls[i] + scroll_change
            new_scroll = int(max(0, min(new_scroll, max_layer_scroll)))  # Clamp
            self.scrolls[i] = int(new_scroll % self.bg_width)
