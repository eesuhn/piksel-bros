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
		self.image = get_image(["terrain"], "stone")
		self.mask = pygame.mask.from_surface(self.image)

		if isinstance(groups[0], pygame.sprite.LayeredUpdates):
			groups[0].change_layer(self, 1)

	def update(self, display: pygame.Surface, offset: pygame.Vector2, **kwargs) -> None:
		"""
		Call in game loop.
		"""

		self.draw(self.image, display, offset)
