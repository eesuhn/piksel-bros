from . import *


class Terrain:
	BLOCK_WIDTH = 64
	BLOCK_HEIGHT = 64

	def __init__(self, x, y) -> None:
		self.rect = pygame.Rect(
			x * Terrain.BLOCK_WIDTH,
			y * Terrain.BLOCK_HEIGHT,
			Terrain.BLOCK_WIDTH,
			Terrain.BLOCK_HEIGHT)
		self.surf = pygame.Surface((Terrain.BLOCK_WIDTH, Terrain.BLOCK_HEIGHT)).convert_alpha()
		self.block = self.get_terrain()
		self.surf.blit(self.block, (0, 0))
		self.mask = pygame.mask.from_surface(self.surf)

	def get_terrain(self) -> pygame.Surface:
		image = get_image(["terrain"], "grass")
		surface = pygame.Surface((Terrain.BLOCK_WIDTH, Terrain.BLOCK_HEIGHT)).convert_alpha()
		rect = pygame.Rect(0, 0, Terrain.BLOCK_WIDTH, Terrain.BLOCK_HEIGHT)
		surface.blit(image, (0, 0), rect)

		return surface

	def draw(self, display: pygame.Surface) -> None:
		display.blit(self.surf, (self.rect.x, self.rect.y))
