from ._internal import *


class Camera(pygame.sprite.LayeredUpdates):
	OFFSET_DELAY = 10

	def __init__(self, level_width, level_height) -> None:
		super().__init__()
		self.level_width = level_width
		self.level_height = level_height
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
		x = (self.target.rect.centerx - SCREEN_WIDTH / 2) - self.offset.x
		y = (self.target.rect.centery - SCREEN_HEIGHT / 2) - self.offset.y

		if self.delay:
			self.offset.x += int(x / self.OFFSET_DELAY)
			self.offset.y += int(y / self.OFFSET_DELAY)
		else:
			self.offset.x += x
			self.offset.y += y

		if self.set_border:
			self.offset.x = max(0, min(self.offset.x, self.level_width - SCREEN_WIDTH))
			self.offset.y = max(0, min(self.offset.y, self.level_height - SCREEN_HEIGHT))

	def get_offset(self, set_border=False, delay=False) -> pygame.Vector2:
		self.set_border = set_border
		self.delay = delay
		self.calc_offset()
		return self.offset
