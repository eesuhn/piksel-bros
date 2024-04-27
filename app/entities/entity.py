from ._internal import *


class Entity(pygame.sprite.Sprite):
	MAX_GRAVITY = 32

	def __init__(self, *groups) -> None:
		super().__init__(*groups)

	def draw(self) -> None:
		"""
		Params:
			`self.display`, `self.image`, `self.rect`, `self.offset`, `self.top_left`
		"""

		self.display.blit(self.image, (
			self.rect.x - self.offset.x - self.top_left.x,
			self.rect.y - self.offset.y - self.top_left.y))

	def gravity(self) -> None:
		"""
		Params:
			`self.vel`, `self.fall_count`
		"""

		max_g = self.MAX_GRAVITY
		self.vel.y += min(1, self.fall_count / (int(max_g * 1.25)))

		if self.fall_count < (int(max_g * 1.25)):
			self.fall_count += 1

		if self.vel.y >= max_g:
			self.vel.y = max_g
