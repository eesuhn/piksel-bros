from . import *


class Entity(pygame.sprite.Sprite):
	def __init__(self, *groups) -> None:
		super().__init__(*groups)

	def gravity(self) -> None:
		"""
		Usage:
			Declare `self.vel.y`, `self.fall_count` in child class.
		"""

		self.vel.y += min(1, self.fall_count / (int(MAX_GRAVITY * 1.25)))
		if self.fall_count < (int(MAX_GRAVITY * 1.25)):
			self.fall_count += 1
		if self.vel.y >= MAX_GRAVITY:
			self.vel.y = MAX_GRAVITY
