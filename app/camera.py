from ._internal import *


class Camera(pygame.sprite.LayeredUpdates):
	OFFSET_DELAY = 10

	def __init__(self, target, level_width, level_height):
		super().__init__()
		self.target = target
		self.add(target)
		self.level_width = level_width
		self.level_height = level_height
		self.offset = pygame.Vector2((0, 0))

	def update(self, display: pygame.Surface, **kwargs):
		x = (self.target.rect.centerx - SCREEN_WIDTH / 2) - self.offset.x
		y = (self.target.rect.centery - SCREEN_HEIGHT / 2) - self.offset.y

		self.offset.x += int(x / self.OFFSET_DELAY)
		self.offset.y += int(y / self.OFFSET_DELAY)

		self.offset.x = max(0, min(self.offset.x, self.level_width - SCREEN_WIDTH))
		self.offset.y = max(0, min(self.offset.y, self.level_height - SCREEN_HEIGHT))

		super().update(display=display, offset=self.offset, **kwargs)
