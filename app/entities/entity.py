from ._internal import *


class Entity(pygame.sprite.Sprite):
	MAX_GRAVITY = 32

	def __init__(self, *groups) -> None:
		super().__init__(*groups)

	def draw(self, image: pygame.Surface, display: pygame.Surface, offset: pygame.Vector2) -> None:
		display.blit(image, (
			self.rect.x - offset.x,
			self.rect.y - offset.y))

	def gravity(self) -> None:
		"""
		Usage:
			Declare `self.vel.y`, `self.fall_count` in child class.
		"""

		max_g = self.MAX_GRAVITY
		self.vel.y += min(1, self.fall_count / (int(max_g * 1.25)))
		if self.fall_count < (int(max_g * 1.25)):
			self.fall_count += 1
		if self.vel.y >= max_g:
			self.vel.y = max_g
