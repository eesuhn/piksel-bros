from ._internal import *
from . import *
from .entities import *


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
		self.init_level()

		while True:
			self.check_event()
			self.loop()
			self.clock.tick(FPS)

	def init_level(self) -> None:
		self.level = [
			"PPPPPPPPPPPPPPPPPPPPPPPPP",
			"P                       P",
			"P                       P",
			"P    PPP     PP         P",
			"P                       P",
			"P                PPP    P",
			"P        PPP            P",
			"P                       P",
			"P            PPP        P",
			"P      PP               P",
			"P  P                    P",
			"P                       P",
			"PPPPPPPPPPPPPPPPPPPPPPPPP",
		]
		level_width = len(self.level[0]) * RECT_WIDTH
		level_height = len(self.level) * RECT_HEIGHT

		self.camera = Camera(level_width, level_height)
		Background(self.camera)
		self.camera.add_target(Player(1, 8, self.camera))
		self.load_level()

	def load_level(self) -> None:
		self.objs = []
		x = y = 0
		for row in self.level:
			for col in row:
				if col == "P":
					self.objs.append(
						Terrain(x, y, self.camera))
				x += 1
			y += 1
			x = 0

	def check_event(self) -> bool:
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

		return True

	def end(self) -> None:
		pygame.quit()
		sys.exit()

	def default_screen_size(self) -> None:
		self.is_fullscreen = False
		pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

	def loop(self) -> None:
		self.display.fill((0, 0, 0))

		self.camera.update(
			display=self.display,
			events=self.events,
			objs=self.objs)

		self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
		pygame.display.update()
