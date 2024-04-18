from ._internal import *
from . import *
from ..utils import *


class Terrain(Entity):
	def __init__(self, x, y, *groups) -> None:
		super().__init__(*groups)
		self.rect = pygame.Rect(
			x * RECT_WIDTH,
			y * RECT_HEIGHT,
			RECT_WIDTH,
			RECT_HEIGHT)
		self.block = self.get_terrain()
		self.mask = pygame.mask.from_surface(self.block)

		if isinstance(groups[0], pygame.sprite.LayeredUpdates):
			groups[0].change_layer(self, 1)

	def get_terrain(self) -> pygame.Surface:
		image = get_image(["terrain"], "block_stone")
		rect = pygame.Rect(0, 0, RECT_WIDTH, RECT_HEIGHT)
		surface = pygame.Surface((RECT_WIDTH, RECT_HEIGHT)).convert_alpha()
		surface.blit(image, (0, 0), rect)

		return surface

	def update(self, display: pygame.Surface, **kwargs) -> None:
		"""
		Call in game loop.
		"""

		display.blit(self.block, (self.rect.x, self.rect.y))
