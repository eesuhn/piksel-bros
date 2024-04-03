from app import *


class Game:
	def __init__(self) -> None:
		pygame.init()
		self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)

	def run(self) -> None:
		self.clock = pygame.time.Clock()

		running = True
		while running:
			running = self.check_event()
			self.loop()
			self.clock.tick(FPS)

		pygame.quit()
		sys.exit()

	def loop(self) -> None:
		self.screen.fill((10, 186, 180))
		pygame.display.update()

	def check_event(self) -> bool:
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					return False

		return True
