import pygame

from typing import TYPE_CHECKING, Any

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
    target: pygame.sprite.Sprite | None

    def __init__(self, *groups: 'Camera'):
        super().__init__(*groups)
        self.target = None

        self.bg_images = []
        self.bg_speeds = []
        self.full_bgs = []
        self.map_width = 0

        if len(groups) > 0 and isinstance(groups[0], pygame.sprite.LayeredUpdates):
            self.map_width = int(groups[0].width)
            groups[0].change_layer(self, 0)

        self.load_bgs()

    def add_target(self, target: pygame.sprite.Sprite) -> None:
        self.target = target

    def load_bgs(self) -> None:
        """
        Load the background images and speeds for each layer
        """
        for i in range(1, 6):
            bg_image = load_image(f'assets/images/background/plx-{i}')
            self.bg_images.append(bg_image)
            speed_factor = 0.6 if i == 1 else (0.4 if i <= 3 else 0.2)
            self.bg_speeds.append(int(i * BG_SPEED * speed_factor))
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
        if not self.target:
            return

        max_scroll = max(0, self.map_width - SCR_W)
        keys = pygame.key.get_pressed()

        # Calculate if target is in scroll zone (center of screen)
        target_x = self.target.rect.centerx
        scroll_threshold = SCR_W // 2

        for i in range(len(self.scrolls)):
            scroll_change = 0

            # Only scroll if target is in the center zone
            if (target_x > scroll_threshold) and (target_x < self.map_width - scroll_threshold):
                if keys[pygame.K_LEFT]:
                    scroll_change = int(-self.bg_speeds[i])
                if keys[pygame.K_RIGHT]:
                    scroll_change = int(self.bg_speeds[i])

            # Scale the scroll change based on the parallax layer
            parallax_factor = (i + 1) / len(self.scrolls)
            max_layer_scroll = max_scroll * parallax_factor

            new_scroll = self.scrolls[i] + scroll_change
            new_scroll = int(max(0, min(new_scroll, max_layer_scroll)))  # Clamp
            self.scrolls[i] = int(new_scroll % self.bg_width)
