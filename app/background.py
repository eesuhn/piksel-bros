from . import *
from .utils import get_image


class Background:
	def __init__(self) -> None:
		backgrounds = [
			filename.replace(".png", "")
			for filename in os.listdir(os.path.join("assets", "background"))
		]
		background = random.choice(backgrounds)
		self.image = get_image(["background"], "green", scale=2)
		self.tile_width = self.image.get_width()
		self.tile_height = self.image.get_height()
		self.num_tiles_x = SCREEN_WIDTH // self.tile_width + 1
		self.num_tiles_y = SCREEN_HEIGHT // self.tile_height + 1
		self.offset_y = 0

	def dim_surface(self, display: pygame.Surface, alpha: int) -> None:
		dim_surf = pygame.Surface(display.get_size()).convert_alpha()
		dim_surf.fill((0, 0, 0, alpha))
		display.blit(dim_surf, (0, 0))

	def get_tiles(self) -> list:
		tiles = []
		for x in range(self.num_tiles_x):
			for y in range(self.num_tiles_y):
				tile_x = x * self.tile_width
				tile_y = (y * self.tile_height) - self.offset_y
				tiles.append((self.image, (tile_x, tile_y)))
		return tiles

	def update_y(self, dt: float) -> None:
		self.offset_y += 0.1 * dt
		if self.offset_y >= self.tile_height:
			self.offset_y -= self.tile_height

	def draw(self, display: pygame.Surface) -> None:
		self.update_y(10)
		for tile in self.get_tiles():
			display.blit(*tile)
		self.dim_surface(display, 30)
