from . import *
from .entities.player import Player
from .objects.block import Block


class Game:
	def __init__(self) -> None:
		pygame.init()
		pygame.display.set_caption("Piksel Bros.")
		self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		self.display = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

	def run(self) -> None:
		self.clock = pygame.time.Clock()
		self.player = Player(1, 2)

		# Objects
		self.objs = [
			Block(1, 8),
			Block(2, 8),
			Block(3, 8),
			Block(4, 8),
			Block(4, 7),
			Block(3, 4),
		]

		while True:
			self.check_event()
			self.loop()
			self.clock.tick(FPS)

	def check_event(self) -> bool:
		self.events = pygame.event.get()

		for event in self.events:
			if event.type == pygame.QUIT:
				self.end()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.end()
				if event.key == pygame.K_F11:
					pygame.display.toggle_fullscreen()

		return True

	def end(self) -> None:
		pygame.quit()
		sys.exit()

	def loop(self) -> None:
		self.display.fill((0, 0, 0))
		self.player.loop(self.events, self.display, self.objs)

		# Objects: Blocks
		for obj in self.objs:
			obj.draw(self.display)

		self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
		pygame.display.update()
