from . import *
from .utils import get_image


class Background:
	def __init__(self) -> None:
		backgrounds = [
			filename.replace(".png", "")
			for filename in os.listdir(os.path.join("assets", "background"))
		]
		background = random.choice(backgrounds)
		self.image = get_image(["background"], background, scale=2)
		self.surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()

		for tile in self.get_tiles():
			self.surf.blit(*tile)

		self.dim_surface(30)

	def dim_surface(self, alpha: int) -> None:
		"""
		Create a dim surface to overlay the background.
		"""

		dim_surf = pygame.Surface(self.surf.get_size()).convert_alpha()
		dim_surf.fill((0, 0, 0, alpha))
		self.surf.blit(dim_surf, (0, 0))

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
