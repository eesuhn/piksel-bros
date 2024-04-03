import pygame
import sys


class Game:
	FPS = 60
	SCREEN_WIDTH = 1280
	SCREEN_HEIGHT = 800

	def __init__(self) -> None:
		pygame.init()
		pygame.display.set_caption("Piksel Bros.")
		self.screen = pygame.display.set_mode((Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT), pygame.NOFRAME)

	# Deprecated: Not suitable for multiple platforms
	def adjust_surf(self) -> None:
		screen_flags = pygame.HWSURFACE | pygame.RESIZABLE | pygame.DOUBLEBUF
		self.screen = pygame.display.set_mode((Game.SCREEN_WIDTH, Game.SCREEN_HEIGHT), screen_flags, 32)
		self.surface = pygame.Surface((Game.CONTENT_WIDTH, Game.CONTENT_HEIGHT))

		window_width, window_height = self.screen.get_size()
		content_aspect_ratio = Game.CONTENT_WIDTH / Game.CONTENT_HEIGHT
		window_aspect_ratio = window_width / window_height

		if content_aspect_ratio > window_aspect_ratio:
			self.scale_factor = window_height / Game.CONTENT_HEIGHT
			scaled_width = int(Game.CONTENT_WIDTH * self.scale_factor)
			scaled_height = window_height
		else:
			self.scale_factor = window_width / Game.CONTENT_WIDTH
			scaled_width = window_width
			scaled_height = int(Game.CONTENT_HEIGHT * self.scale_factor)

		self.scaled_surface = pygame.transform.scale(self.surface, (scaled_width, scaled_height))

		self.surf_x = (window_width - scaled_width) // 2
		self.surf_y = (window_height - scaled_height) // 2

	def run(self) -> None:
		self.clock = pygame.time.Clock()

		running = True
		while running:
			running = self.check_event()
			self.loop()

		pygame.quit()
		sys.exit()

	def loop(self) -> None:
		self.screen.fill((10, 186, 180))
		pygame.display.update()
		self.clock.tick(Game.FPS)

	def check_event(self) -> bool:
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					return False

		return True
