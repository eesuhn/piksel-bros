import pygame


class Game:
	FPS = 60
	WIDTH = 1280
	HEIGHT = 720

	def __init__(self) -> None:
		pygame.init()
		self.window = pygame.display.set_mode((Game.WIDTH, Game.HEIGHT), pygame.NOFRAME)

	def run(self) -> None:
		clock = pygame.time.Clock()

		run = True
		while run:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False
					break
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						run = False
						break

			clock.tick(Game.FPS)

		pygame.quit()
		quit()
