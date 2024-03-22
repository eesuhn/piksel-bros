import sys
import pygame
from .entities.player import Player
from .utils import load_img, load_imgs
from .map import Map


class Game:
	FPS = 60
	WIDTH = 1280
	HEIGHT = 720

	def __init__(self):
		pygame.init()
		pygame.display.set_caption("Piksel Bros.")
		self.window = pygame.display.set_mode((Game.WIDTH, Game.HEIGHT))
		self.clock = pygame.time.Clock()
		self.assets = {
			'dirt': load_imgs('terrain/dirt'),
			'player': load_img('main_characters/player.png', 4)
		}
		self.player = Player(self)
		self.map = Map(self)

	def run(self):
		while True:
			self.loop()

			for event in pygame.event.get():
				if not self.event(event):
					break

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
		# TEMP : Background
		self.window.fill((10, 186, 180))
		self.map.render(self.window)
		self.player.move(self.window)
