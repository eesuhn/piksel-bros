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
		image = get_image(["terrain"], "grass")
		surface = pygame.Surface((BLOCK_WIDTH, BLOCK_HEIGHT)).convert_alpha()
		rect = pygame.Rect(0, 0, BLOCK_WIDTH, BLOCK_HEIGHT)
		surface.blit(image, (0, 0), rect)

		return surface

	def draw(self, display: pygame.Surface, offset=(0, 0)) -> None:
		pos_x = self.rect.x - offset[0] - OFFSET_DELAY
		pos_y = self.rect.y - offset[1] - OFFSET_DELAY

		display.blit(self.surf, (pos_x, pos_y + Y_OFFSET))
