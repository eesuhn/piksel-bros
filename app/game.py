from ._internal import *
from .entities import *
from .camera import Camera
from .level import Level


class Game:
	def __init__(self) -> None:
		self._ignore_warnings()

		pygame.init()
		pygame.display.set_caption("Piksel Bros.")

		screen_flags = pygame.DOUBLEBUF | pygame.HWSURFACE
		self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), screen_flags)
		self.display = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()
		self.is_fullscreen = False

	def _ignore_warnings(self) -> None:
		"""
		Ignore warnings from `pygame`
		"""
		message = [
			"re-creating window in toggle_fullscreen",
		]
		for m in message:
			warnings.filterwarnings("ignore", message=m)

	def run(self) -> None:
		self.clock = pygame.time.Clock()
		self.level = Level()
		self._load_level()

		while True:
			self._check_event()
			self._loop()
			self.clock.tick(FPS)

	def _load_level(self) -> None:
		self.level.init_level("01")

		width, height = self.level.get_size()
		self.top_left, self.bottom_right = self.level.get_min_max()
		self.camera = Camera(width, height)

		player_name = self.level.get_player_name()
		self.player_pos = self.level.get_player_pos()
		self.player = Player(player_name, self.player_pos.x, self.player_pos.y, self.camera)

		self.objs = self.level.load(self.camera, self.player)

	def _check_event(self) -> None:
		self.events = pygame.event.get()

		for event in self.events:
			if event.type == pygame.QUIT:
				self._end()
			if event.type == pygame.KEYDOWN:
				self._handle_keydown(event)

	def _handle_keydown(self, event: pygame.event.Event) -> None:
		if event.key == pygame.K_ESCAPE:
			if not self.is_fullscreen:
				self._end()
			else:
				self._default_screen_size()
		if event.key == pygame.K_F11:
			if not self.is_fullscreen:
				self.is_fullscreen = True
				pygame.display.toggle_fullscreen()
			else:
				self._default_screen_size()

	def _end(self) -> None:
		pygame.quit()
		sys.exit()

	def _default_screen_size(self) -> None:
		self.is_fullscreen = False
		pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

	def _loop(self) -> None:
		self.display.fill((0, 0, 0))

		self.camera.update(
			events=self.events,
			display=self.display,
			objs=self.objs,
			top_left=self.top_left,
			bottom_right=self.bottom_right,
			set_border=True,
			delay=True)

		self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
		pygame.display.update()
