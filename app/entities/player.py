import pygame
from .physics import Physics


class Player(Physics):
	def __init__(self, game):
		self.physics = Physics(game, 'player', (50, 50), (8, 16))
		self.vel = 10

	def move(self, window):
		key = pygame.key.get_pressed()
		self.physics.update(((key[pygame.K_RIGHT] - key[pygame.K_LEFT]) * self.vel, 0))
		self.physics.render(window)
