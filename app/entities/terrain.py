from ._internal import *
from .entity import Entity
from ..utils import *


class Terrain(Entity):
	def __init__(self, type: str, var: int, x, y, *groups) -> None:
		super().__init__(*groups)
		self.rect = pygame.Rect(
			x * RECT_WIDTH,
			y * RECT_HEIGHT,
			RECT_WIDTH,
			RECT_HEIGHT)
		self.image = get_image(["terrain", type], f"{var}")
		self.mask = pygame.mask.from_surface(self.image)

		if len(groups) > 0 and isinstance(groups[0], pygame.sprite.LayeredUpdates):
			groups[0].change_layer(self, 1)

	def update(self, **kwargs) -> None:
		"""
		Call in game loop.
		"""

		for k, v in kwargs.items():
			setattr(self, k, v)

		self.draw()
