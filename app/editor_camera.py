from ._internal import *


class EditorCamera(pygame.sprite.Sprite):
	CAM_VEL = 20

	def __init__(self, x, y, *groups) -> None:
		super().__init__(*groups)
		self.rect = pygame.Rect(x, y, SCREEN_WIDTH, SCREEN_HEIGHT)
		self.image = pygame.Surface((
			SCREEN_WIDTH * CAM_SCALE,
			SCREEN_HEIGHT * CAM_SCALE)).convert_alpha()
		self.scroll = pygame.Vector2((x, y))

		if len(groups) > 0 and isinstance(groups[0], pygame.sprite.LayeredUpdates):
			groups[0].change_layer(self, 2)

	def update(self, **kwargs) -> None:
		"""
		Call in game loop
		"""
		for k, v in kwargs.items():
			setattr(self, k, v)

		self._draw()
		self._move()

	def _draw(self) -> None:
		self.image.fill((0, 0, 0, 0))

		self._draw_current_obj()

		self.display.blit(self.image, (0, 0))

	def _draw_current_obj(self) -> None:
		self.image.blit(
			self.current_obj, (
				(20) * CAM_SCALE,
				(SCREEN_HEIGHT - 60) * CAM_SCALE))

	def _move(self) -> None:
		keys = pygame.key.get_pressed()
		dir_x = (keys[pygame.K_d] - keys[pygame.K_a]) * self.CAM_VEL
		dir_y = (keys[pygame.K_s] - keys[pygame.K_w]) * self.CAM_VEL

		# Normalize diagonal movement
		if dir_x != 0 and dir_y != 0:
			dir_x *= 0.7071
			dir_y *= 0.7071

		self.rect.x += dir_x
		self.rect.y += dir_y
		self.scroll.x += dir_x
		self.scroll.y += dir_y
		self._set_border()

	def _set_border(self) -> None:
		self.rect.x = max(0, self.rect.x)
		self.rect.y = max(0, self.rect.y)
		self.scroll.x = max(0, self.scroll.x)
		self.scroll.y = max(0, self.scroll.y)

	def mpos_to_wpos(self, o_screen: pygame.Vector2) -> pygame.Vector2:
		"""
		Returns world position based on mouse position
		"""
		mpos = pygame.Vector2(pygame.mouse.get_pos())
		ratio_x = SCREEN_WIDTH * CAM_SCALE / o_screen.x
		ratio_y = SCREEN_HEIGHT * CAM_SCALE / o_screen.y
		adjust = pygame.Vector2((mpos.x * ratio_x, mpos.y * ratio_y))

		return pygame.Vector2((
			(adjust.x + self.scroll.x) // RECT_WIDTH,
			(adjust.y + self.scroll.y) // RECT_HEIGHT))
