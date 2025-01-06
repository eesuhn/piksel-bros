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

    def __init__(self, *groups: 'Camera'):
        super().__init__(*groups)

        self.bg_images = []
        self.bg_speeds = []
        self.load_bgs()

        if len(groups) > 0 and isinstance(groups[0], pygame.sprite.LayeredUpdates):
            groups[0].change_layer(self, 0)

    def load_bgs(self) -> None:
        for i in range(1, 6):
            bg_image = load_image(f'assets/images/background/plx-{i}')
            self.bg_images.append(bg_image)
            self.bg_speeds.append(i * 0.2)
        self.scrolls = [0] * len(self.bg_images)
        self.bg_width = self.bg_images[0].get_width()

    def update(self, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

        self.draw_bgs()
        self.scroll()

    def draw_bgs(self) -> None:
        for i, image in enumerate(self.bg_images):
            for x in range(5):
                self.display.blit(
                    image,
                    ((x * self.bg_width) - self.scrolls[i], 0)
                )

    def scroll(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            for i in range(len(self.scrolls)):
                self.scrolls[i] -= int(BG_SPEED * self.bg_speeds[i])
        if keys[pygame.K_RIGHT]:
            for i in range(len(self.scrolls)):
                self.scrolls[i] += int(BG_SPEED * self.bg_speeds[i])

        # Wrap scroll values for horizontal looping
        for i in range(len(self.scrolls)):
            self.scrolls[i] %= self.bg_width
