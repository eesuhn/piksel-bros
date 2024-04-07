from . import *
from .utils import get_image


class Background:
	def __init__(self) -> None:
		self.image = get_image(["background"], "green", scale=2)
		self.surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

		for tile in self.get_tiles():
			self.surf.blit(*tile)

	def get_tiles(self) -> list:
		tiles = []
		width = self.image.get_width()
		height = self.image.get_height()

		for x in range(SCREEN_WIDTH // width + 1):
			for y in range(SCREEN_HEIGHT // height + 1):
				tiles.append((self.image, (x * width, y * height)))

		return tiles

	def draw(self, display: pygame.Surface) -> None:
		display.blit(self.surf, (0, 0))
