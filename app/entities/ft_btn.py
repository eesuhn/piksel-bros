import pygame


class FtBtn:
	def __init__(self, x=100, y=100):
		self.btn = pygame.transform.scale(
			(pygame.image.load('assets/menu/buttons/next.png')),
			(64, 64))
		self.btn_pos = [x, y]

	def move(self, window, vel=1):
		key = pygame.key.get_pressed()
		self.btn_pos[0] += (key[pygame.K_RIGHT] - key[pygame.K_LEFT]) * vel
		self.btn_pos[1] += (key[pygame.K_DOWN] - key[pygame.K_UP]) * vel
		window.blit(self.btn, self.btn_pos)
