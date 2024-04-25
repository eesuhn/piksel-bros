from ._internal import *


class Camera(pygame.sprite.LayeredUpdates):
	OFFSET_DELAY = 10

	def __init__(self, width=0, height=0) -> None:
		super().__init__()
		self.width = width
		self.height = height
		self.offset = pygame.Vector2((0, 0))
		self.set_border = False
		self.delay = False

	def add_target(self, target) -> None:
		self.target = target

	def update(self, **kwargs) -> None:
		for k, v in kwargs.items():
			setattr(self, k, v)

		self.calc_offset()

		super().update(offset=self.offset, **kwargs)

	def calc_offset(self) -> None:
		"""
		Params:
			`self.set_border`, `self.delay`
		"""

		x = (-SCREEN_WIDTH // 2) + self.target.rect.centerx - self.offset.x
		y = (-SCREEN_HEIGHT // 2) + self.target.rect.centery - self.offset.y

		if self.delay:
			self.offset.x += int(x / self.OFFSET_DELAY)
			self.offset.y += int(y / self.OFFSET_DELAY)
		else:
			self.offset.x += x
			self.offset.y += y

		if self.set_border:
			self.offset.x = max(0, min(self.offset.x, self.width - SCREEN_WIDTH))
			self.offset.y = max(0, min(self.offset.y, self.height - SCREEN_HEIGHT))
