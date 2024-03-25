import pygame
from .physics import Physics


class Player(Physics):
	def __init__(self, game, pos):
		super().__init__(game, 'player', pos, (8, 16))
		self.game = game
		self.vel = 10

	def move(self):
		key = pygame.key.get_pressed()
		self.update(((key[pygame.K_RIGHT] - key[pygame.K_LEFT]) * self.vel, 0))
		self.render()

	def render(self):
		self.game.window.blit(self.game.assets['player'], self.pos)
