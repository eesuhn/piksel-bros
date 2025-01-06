import pygame

from typing import TYPE_CHECKING, Any

from ..utils import load_image
from ._constants import BG_SPEED

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
        self.load_bgs()

        if len(groups) > 0 and isinstance(groups[0], pygame.sprite.LayeredUpdates):
            groups[0].change_layer(self, 0)

    def load_bgs(self) -> None:
        for i in range(1, 6):
            bg_image = load_image(f'assets/images/background/plx-{i}')
            self.bg_images.append(bg_image)
            self.bg_speeds.append(int(i * 0.2 * BG_SPEED))
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
            # Calculate source and destination rects
            scroll = self.scrolls[i]
            source_rect = pygame.Rect(scroll, 0, display_rect.width, display_rect.height)
            self.display.blit(full_bg, (0, 0), source_rect)

    def scroll(self) -> None:
        keys = pygame.key.get_pressed()
        for i in range(len(self.scrolls)):
            if keys[pygame.K_LEFT]:
                self.scrolls[i] = int((self.scrolls[i] - self.bg_speeds[i]) % self.bg_width)
            if keys[pygame.K_RIGHT]:
                self.scrolls[i] = int((self.scrolls[i] + self.bg_speeds[i]) % self.bg_width)
