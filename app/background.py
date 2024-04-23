from ._internal import *
from .utils import *


class Background(pygame.sprite.Sprite):
	BG_VEL = 10
	BG_OPACITY = 215

	def __init__(self, var: str, *groups) -> None:
		super().__init__(*groups)
		self.image = get_image(["background"], var, scale=2)
		self.image.set_alpha(self.BG_OPACITY)
		self.tile_width = self.image.get_width()
		self.tile_height = self.image.get_height()
		self.num_tiles_x = SCREEN_WIDTH // self.tile_width + 1
		self.num_tiles_y = SCREEN_HEIGHT // self.tile_height + 1
		self.offset_y = 0

		if isinstance(groups[0], pygame.sprite.LayeredUpdates):
			groups[0].change_layer(self, 0)

	def get_tiles(self) -> list:
		tiles = []
		for x in range(self.num_tiles_x):
			for y in range(self.num_tiles_y):
				tile_x = x * self.tile_width
				tile_y = (y * self.tile_height) - self.offset_y
				tiles.append((self.image, (tile_x, tile_y)))
		return tiles

	def update_y(self) -> None:
		self.offset_y += 0.1 * self.BG_VEL
		if self.offset_y >= self.tile_height:
			self.offset_y -= self.tile_height

	def update(self, **kwargs) -> None:
		"""
		Call in game loop.
		"""

		for k, v in kwargs.items():
			setattr(self, k, v)

		self.update_y()
		for tile in self.get_tiles():
			self.display.blit(*tile)
