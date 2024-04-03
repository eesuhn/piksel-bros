from app import *


class Game:
	def __init__(self) -> None:
		pygame.init()
		pygame.display.set_caption("Piksel Bros.")
		self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		self.display = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

	def run(self) -> None:
		self.clock = pygame.time.Clock()

		while True:
			self.check_event()
			self.loop()
			self.clock.tick(FPS)

	def check_event(self) -> bool:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.end()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.end()

		return True

	def end(self) -> None:
		pygame.quit()
		sys.exit()

	def loop(self) -> None:
		...
		self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
		pygame.display.update()
