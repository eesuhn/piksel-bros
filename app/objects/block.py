from . import *
from ..utils import get_image


class Block:
	def __init__(self, x, y) -> None:
		self.rect = pygame.Rect(
			x * BLOCK_WIDTH,
			y * BLOCK_HEIGHT,
			BLOCK_WIDTH,
			BLOCK_HEIGHT)
		self.surf = pygame.Surface((BLOCK_WIDTH, BLOCK_HEIGHT)).convert_alpha()
		self.block = self.get_block()
		self.surf.blit(self.block, (0, 0))
		self.mask = pygame.mask.from_surface(self.surf)

	def get_block(self) -> pygame.Surface:
		blocks = [
			filename.replace(".png", "")
			for filename in os.listdir(os.path.join("assets", "terrain"))
		]
		block = random.choice(blocks)
		image = get_image(["terrain"], "grass")
		surface = pygame.Surface((BLOCK_WIDTH, BLOCK_HEIGHT)).convert_alpha()
		rect = pygame.Rect(0, 0, BLOCK_WIDTH, BLOCK_HEIGHT)
		surface.blit(image, (0, 0), rect)

		return surface

	def draw(self, display: pygame.Surface) -> None:
		display.blit(self.surf, (self.rect.x, self.rect.y))
