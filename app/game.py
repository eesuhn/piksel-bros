import sys
import pygame
from .entities.ft_btn import FtBtn


class Game:
	FPS = 60
	WIDTH = 1280
	HEIGHT = 720

	def __init__(self):
		pygame.init()
		pygame.display.set_caption("Piksel Bros.")
		self.surface = pygame.display.set_mode((Game.WIDTH, Game.HEIGHT))
		self.clock = pygame.time.Clock()
		# btn
		self.btn = FtBtn(0, 0)

	def run(self):
		while True:
			self.loop()

			for event in pygame.event.get():
				if not self.event(event):
					break

			# I don't know what is this for
			pygame.display.update()
			self.clock.tick(Game.FPS)

	def stop(self):
		pygame.quit()
		sys.exit()

	def event(self, event):
		if event.type == pygame.QUIT:
			self.stop()
			return False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				self.stop()
				return False

		return True

	def loop(self):
		self.surface.fill((0, 0, 0))
		# btn
		self.btn.move(self.surface, 10)
