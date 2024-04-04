from . import *
from ..utils import get_sprites


class Player:
	WIDTH = 32
	HEIGHT = 32

	def __init__(self, pos_x, pos_y) -> None:
		self.rect = pygame.Rect(pos_x, pos_y, self.WIDTH, self.HEIGHT)
		self.sprites = get_sprites(
			["main_characters", "ninja_frog"],
			self.WIDTH,
			self.HEIGHT,
			direction=True)

	def update_sprite(self) -> None:
		...
