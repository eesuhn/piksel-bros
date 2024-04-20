from ._internal import *
from .entities import *
from .game import Game
from .camera import Camera
from .level import Level


class Editor(Game):
	def __init__(self) -> None:
		super().__init__()
		pygame.display.set_caption("Editor - Piksel Bros.")
		self.display = pygame.Surface((
			SCREEN_WIDTH * 1.6,
			SCREEN_HEIGHT * 1.6)).convert_alpha()

	def load_level(self) -> None:
		level = Level()
		width, height = level.get_size("01")
		self.camera = Camera(width, height)
		self.camera.add_target(
			EditorCamera(
				width // 2,
				height // 2,
				self.camera))
		level.init_level("01", self.camera, target_player=False)

	def loop(self) -> None:
		self.display.fill((0, 0, 0))

		self.camera.update(
			display=self.display,
			events=self.events,
			set_border=False)

		self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
		pygame.display.update()


class EditorCamera(pygame.sprite.Sprite):
	CAM_VEL = 20

	def __init__(self, x, y, *groups) -> None:
		super().__init__(*groups)
		self.rect = pygame.Rect(x, y, 1, 1)

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
