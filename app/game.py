from . import *
from .entities.player import Player
from .objects.block import Block
from .background import Background


class Game:
	def __init__(self) -> None:
		pygame.init()
		pygame.time.set_timer(CPU_MONITOR_EVENT, 1000)
		pygame.display.set_caption("Piksel Bros.")
		self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		self.display = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()
		self.is_fullscreen = False

	def check_cpu(self) -> None:
		print(f"CPU: {psutil.cpu_percent()}%")

	def run(self) -> None:
		self.clock = pygame.time.Clock()
		self.background = Background()
		self.player = Player(1, 1)

		# Objects
		self.objs = []

		i = 0
		while i < 20:
			self.objs.append(Block(i, 9))
			i += 1

		self.objs.append(Block(4, 8))
		self.objs.append(Block(9, 6))

		while True:
			self.check_event()
			self.loop()
			self.clock.tick(FPS)

	def check_event(self) -> bool:
		self.events = pygame.event.get()

		for event in self.events:
			if event.type == CPU_MONITOR_EVENT:
				self.check_cpu()
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
		self.background.draw(self.display)
		self.player.loop(self.events, self.display, self.objs)

		# Objects: Block
		for obj in self.objs:
			obj.draw(self.display)

		self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
		pygame.display.update()
