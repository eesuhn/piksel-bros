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

	def load_level(self) -> None:
		width, height, min_x, min_y, _, _ = self.level.get_size(get_x_y=True)
		self.top_left = (min_x * RECT_WIDTH, min_y * RECT_HEIGHT)
		self.camera = Camera(width, height)

		self.camera.add_target(
			EditorCamera(
				int(width * 0.3),
				int(height * 0.3),
				self.camera))

		self.level.init_level(self.camera, target_player=False)

	def loop(self) -> None:
		self.display.fill((0, 0, 0))
		self.check_mouse()

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

	def border(self) -> None:
		offset = self.camera.get_offset()
		width, height = self.level.get_size()
		pygame.draw.rect(self.display, (255, 0, 0, 128), (
			0 - offset.x,
			0 - offset.y,
			width,
			height), 2)

	def check_mouse(self) -> None:
		mpos = pygame.Vector2(pygame.mouse.get_pos())


class EditorCamera(pygame.sprite.Sprite):
	CAM_VEL = 20

	def __init__(self, x, y, *groups) -> None:
		super().__init__(*groups)
		self.rect = pygame.Rect(x, y, 10, 10)

	def update(self, **kwargs) -> None:
		self.move()

	def move(self) -> None:
		keys = pygame.key.get_pressed()
		dx, dy = 0, 0

		if keys[pygame.K_LEFT]:
			dx -= self.CAM_VEL
		if keys[pygame.K_RIGHT]:
			dx += self.CAM_VEL
		if keys[pygame.K_UP]:
			dy -= self.CAM_VEL
		if keys[pygame.K_DOWN]:
			dy += self.CAM_VEL

		if dx != 0 and dy != 0:
			dx *= 0.7071
			dy *= 0.7071

		self.rect.x += dx
		self.rect.y += dy
