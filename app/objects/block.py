from . import *
from ..utils import get_image


class Block:
	def __init__(self, x, y) -> None:
		x *= BLOCK_WIDTH
		y *= BLOCK_HEIGHT
		self.rect = pygame.Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT)
		self.surf = pygame.Surface((BLOCK_WIDTH, BLOCK_HEIGHT), pygame.SRCALPHA)
		self.block = self.get_block()
		self.surf.blit(self.block, (0, 0))
		self.mask = pygame.mask.from_surface(self.surf)

	def get_block(self) -> pygame.Surface:
		image = get_image(["terrain"], "grass")
		surface = pygame.Surface((BLOCK_WIDTH, BLOCK_HEIGHT), pygame.SRCALPHA)
		rect = pygame.Rect(0, 0, BLOCK_WIDTH, BLOCK_HEIGHT)
		surface.blit(image, (0, 0), rect)

		return surface

	def draw(self, display: pygame.Surface) -> None:
		display.blit(self.surf, (self.rect.x, self.rect.y))
