from . import *


class Camera:
	def __init__(self) -> None:
		self.offset = [0, 0]
		self.x_offset = DEFAULT_OFFSET[0]
		self.y_offset = DEFAULT_OFFSET[1]

	def get_offset(self, display: pygame.Surface, target) -> tuple:
		self.offset[0] += (
			target.rect.centerx - display.get_width() / 2 - self.offset[0]) / (
			OFFSET_DELAY * 2)
		self.offset[1] += (
			target.rect.centery - display.get_height() / 2 - self.offset[1]) / (
			OFFSET_DELAY)

		return (
			int(self.offset[0]) + OFFSET_DELAY - self.x_offset,
			int(self.offset[1]) + OFFSET_DELAY - self.y_offset)
