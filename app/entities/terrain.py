from . import *
from .entity import Entity


class Terrain(Entity):
	BLOCK_WIDTH = 64
	BLOCK_HEIGHT = 64

	def __init__(self, x, y, *groups) -> None:
		super().__init__(*groups)
		self.rect = pygame.Rect(
			x * Terrain.BLOCK_WIDTH,
			y * Terrain.BLOCK_HEIGHT,
			Terrain.BLOCK_WIDTH,
			Terrain.BLOCK_HEIGHT)
		self.block = self.get_terrain()
		self.mask = pygame.mask.from_surface(self.block)

	def get_terrain(self) -> pygame.Surface:
		image = get_image(["terrain"], "block_stone")
		rect = pygame.Rect(0, 0, Terrain.BLOCK_WIDTH, Terrain.BLOCK_HEIGHT)
		surface = pygame.Surface((Terrain.BLOCK_WIDTH, Terrain.BLOCK_HEIGHT)).convert_alpha()
		surface.blit(image, (0, 0), rect)

		return surface

	def update(self, display: pygame.Surface, **kwargs) -> None:
		"""
		Call in game loop.
		"""

		display.blit(self.block, (self.rect.x, self.rect.y))
