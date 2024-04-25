from ._internal import *
from .entities import *
from .game import Game
from .camera import Camera


class Editor(Game):
	def __init__(self) -> None:
		super().__init__()
		pygame.display.set_caption("Editor - Piksel Bros.")
		self.display = pygame.Surface((
			SCREEN_WIDTH * CAM_SCALE,
			SCREEN_HEIGHT * CAM_SCALE)).convert_alpha()
		self.left_click = False
		self.right_click = False
		self.wpos = pygame.Vector2((0, 0))
		self.o_screen = pygame.Vector2((self.screen.get_size()))

	def load_level(self) -> None:
		self.level.init_level("01")

		width, height = self.level.get_size()
		self.camera = Camera(width, height)
		self.top_left, _ = self.level.get_min_max()

		self.editor_camera = EditorCamera(0, 0, self.camera)
		self.camera.add_target(self.editor_camera)
		self.level.load(self.camera, target_player=False)

	def loop(self) -> None:
		self.display.fill((0, 0, 0))

		self.check_mouse()
		self.camera.update(
			display=self.display)

		self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
		pygame.display.update()

	def check_event(self) -> None:
		super().check_event()

		for event in self.events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					self.level.save()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1 and not self.right_click:
					self.left_click = True
				if event.button == 3 and not self.left_click:
					self.right_click = True
			if event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
					self.left_click = False
				if event.button == 3:
					self.right_click = False
			if event.type == pygame.VIDEORESIZE:
				self.o_screen = pygame.Vector2((event.w, event.h))

	def check_mouse(self) -> None:
		self.wpos = self.editor_camera.mpos_to_wpos(self.o_screen, self.top_left)
		x = int(self.wpos.x)
		y = int(self.wpos.y)

		if self.left_click:
			self.add_block(x, y)
		if self.right_click:
			self.remove_block(x, y)

	def add_block(self, x, y) -> None:
		key = f"{x};{y}"
		if key in self.level.on_grid:
			return

		self.level.on_grid[key] = {
			"type": "stone",
			"var": 1,
			"pos": [x, y]}
		self.level.load_added(x, y)

	def remove_block(self, x, y) -> None:
		key = f"{x};{y}"
		if key in self.level.on_grid:
			del self.level.on_grid[key]
			self.level.load_removed(x, y)


class EditorCamera(pygame.sprite.Sprite):
	CAM_VEL = 20

	def __init__(self, x, y, *groups) -> None:
		super().__init__(*groups)
		self.rect = pygame.Rect(x, y, 2, 2)
		self.scroll = pygame.Vector2((0, 0))

	def update(self, **kwargs) -> None:
		self.move()

	def move(self) -> None:
		keys = pygame.key.get_pressed()
		dir_x = (keys[pygame.K_d] - keys[pygame.K_a]) * self.CAM_VEL
		dir_y = (keys[pygame.K_s] - keys[pygame.K_w]) * self.CAM_VEL

		if dir_x != 0 and dir_y != 0:
			dir_x *= 0.7071
			dir_y *= 0.7071

		self.rect.x += dir_x
		self.rect.y += dir_y
		self.scroll.x += dir_x
		self.scroll.y += dir_y

	def mpos_to_wpos(self, o_screen: pygame.Vector2, top_left: pygame.Vector2) -> pygame.Vector2:
		"""
		Returns world position based on mouse position.
		"""

		mpos = pygame.Vector2(pygame.mouse.get_pos())
		ratio_x = SCREEN_WIDTH * CAM_SCALE / o_screen.x
		ratio_y = SCREEN_HEIGHT * CAM_SCALE / o_screen.y
		adjust = pygame.Vector2((mpos.x * ratio_x, mpos.y * ratio_y))

		# -8, -5 prob. due to 16/10 ratio.
		return pygame.Vector2((
			int((adjust.x + self.scroll.x) / RECT_WIDTH) + (top_left.x // RECT_WIDTH) - 8,
			int((adjust.y + self.scroll.y) / RECT_HEIGHT) + (top_left.y // RECT_HEIGHT) - 5))
