import math
import pygame


class Physics:
	def __init__(self, game, e_type, pos, size):
		self.game = game
		self.e_type = e_type
		self.pos = list(pos)
		self.size = size
		self.x_vel = 0
		self.y_vel = 0
		self.gravity_acc = 0

	def rect(self):
		return pygame.Rect(*self.pos, *self.size)

	def update(self, mov=(0, 0)):
		frame_mov = (mov[0] + self.x_vel, mov[1] + self.y_vel)
		entity_rect = self.rect()

		self.pos[0] += frame_mov[0]
		for rect in self.game.map.physics_rects_around(self.pos):
			if entity_rect.colliderect(rect):
				if frame_mov[0] > 0:
					entity_rect.right = rect.left
				if frame_mov[0] < 0:
					entity_rect.left = rect.right
				self.pos[0] = entity_rect.x

		self.pos[1] += frame_mov[1]
		for rect in self.game.map.physics_rects_around(self.pos):
			if entity_rect.colliderect(rect):
				if frame_mov[1] > 0:
					entity_rect.bottom = rect.top
				if frame_mov[1] < 0:
					entity_rect.top = rect.bottom
				self.pos[1] = entity_rect.y

		self.y_vel = min(5, self.y_vel + 0.2)
		# self.apply_gravity()

	def apply_gravity(self):
		self.y_vel = round(min(20, self.y_vel + math.sqrt(self.gravity_acc)), 1)
		self.gravity_acc = round(min(2, self.gravity_acc + 0.2), 1)
		self.pos[1] += self.y_vel
