from ._internal import *
from .entities import *
from .game import Game
from .camera import Camera


class Editor(Game):
	def __init__(self) -> None:
		super().__init__()
		pygame.display.set_caption("Editor - Piksel Bros.")
		self.left_click = False
		self.right_click = False
		self.o_screen = pygame.Vector2((self.screen.get_size()))

	def load_level(self) -> None:
		width, height, min_x, min_y, _, _ = self.level.get_size(get_x_y=True)
		self.top_left = (min_x * RECT_WIDTH, min_y * RECT_HEIGHT)
		self.camera = Camera(width, height)

		self.editor_camera = EditorCamera(0, 0, self.camera)
		self.camera.add_target(self.editor_camera)
		self.level.init_level(self.camera, target_player=False)

	def loop(self) -> None:
		self.display.fill((0, 0, 0))

		self.camera.update(
			display=self.display,
			top_left=self.top_left)

		self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
		pygame.display.update()

	def check_event(self) -> None:
		super().check_event()

		for event in self.events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1 and not self.right_click:
					self.left_click = True
				if event.button == 3 and not self.left_click:
					self.right_click = True
				if event.button == 4:
					...
				if event.button == 5:
					...
			if event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
					self.left_click = False
				if event.button == 3:
					self.right_click = False
			if event.type == pygame.VIDEORESIZE:
				self.o_screen = pygame.Vector2((event.w, event.h))

	def border(self) -> None:
		offset = self.camera.get_offset()
		width, height = self.level.get_size()
		pygame.draw.rect(self.display, (255, 0, 0, 128), (
			0 - offset.x,
			0 - offset.y,
			width,
			height), 2)


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

	def mpos_to_wpos(self, o_screen: pygame.Vector2) -> tuple:
		"""
		Returns world position based on mouse position.
		"""

		mpos = pygame.Vector2(pygame.mouse.get_pos())

		ratio_x = SCREEN_WIDTH / o_screen.x
		ratio_y = SCREEN_HEIGHT / o_screen.y
		adjust = pygame.Vector2((mpos.x * ratio_x, mpos.y * ratio_y))

		w_pos_x = int((adjust.x + self.scroll.x) / RECT_WIDTH) - 8
		w_pos_y = int((adjust.y + self.scroll.y) / RECT_HEIGHT) - 5

		return w_pos_x, w_pos_y
