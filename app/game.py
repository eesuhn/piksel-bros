from ._internal import *
from .entities import *
from .camera import Camera
from .level import Level


class Game:
	def __init__(self) -> None:
		self.ignore_warnings()
		pygame.init()
		pygame.time.set_timer(CPU_MONITOR_EVENT, 1000)
		pygame.display.set_caption("Piksel Bros.")
		screen_flags = pygame.DOUBLEBUF | pygame.HWSURFACE
		self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), screen_flags)
		self.display = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()
		self.is_fullscreen = False
		self.check_cpu = "--cpu" in sys.argv

	def ignore_warnings(self) -> None:
		"""
		Ignore warnings from `pygame`.
		"""

		message = [
			"re-creating window in toggle_fullscreen",
		]
		for m in message:
			warnings.filterwarnings("ignore", message=m)

	def cpu(self, event_type: int) -> None:
		"""
		Check CPU usage when "--cpu" is passed as an argument.
		"""

		if self.check_cpu and event_type == CPU_MONITOR_EVENT:
			print(f"CPU: {psutil.cpu_percent()}%")

	def run(self) -> None:
		self.clock = pygame.time.Clock()
		self.level = Level()
		self.load_level()

		while True:
			self.check_event()
			self.loop()
			self.clock.tick(FPS)

	def load_level(self) -> None:
		self.level.load("02")

		width, height, min_x, min_y, _, _ = self.level.get_size(get_x_y=True)
		self.top_left = pygame.Vector2((min_x * RECT_WIDTH, min_y * RECT_HEIGHT))
		self.camera = Camera(width, height)

		self.objs = self.level.init_level(self.camera)

	def check_event(self) -> None:
		self.events = pygame.event.get()

		for event in self.events:
			self.cpu(event.type)
			if event.type == pygame.QUIT:
				self.end()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					if not self.is_fullscreen:
						self.end()
					else:
						self.default_screen_size()
				if event.key == pygame.K_F11:
					if not self.is_fullscreen:
						self.is_fullscreen = True
						pygame.display.toggle_fullscreen()
					else:
						self.default_screen_size()

	def end(self) -> None:
		pygame.quit()
		sys.exit()

	def default_screen_size(self) -> None:
		self.is_fullscreen = False
		pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

	def loop(self) -> None:
		self.display.fill((0, 0, 0))

		self.camera.update(
			events=self.events,
			display=self.display,
			top_left=self.top_left,
			objs=self.objs,
			set_border=True,
			delay=True)

		self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
		pygame.display.update()
