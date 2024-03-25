import math


class Physics:
	def __init__(self, game, e_type, pos, size):
		self.game = game
		self.e_type = e_type
		self.pos = list(pos)
		self.size = size
		self.y_vel = 0
		self.gravity_acc = 0

	def update(self, mov=(0, 0)):
		self.pos[0] += mov[0]
		self.pos[1] += mov[1]
		self.apply_gravity()

	# def render(self, surf):
	# 	surf.blit(self.game.assets['player'], self.pos)

	def apply_gravity(self):
		self.y_vel = round(min(20, self.y_vel + math.sqrt(self.gravity_acc)), 1)
		self.gravity_acc = round(min(2, self.gravity_acc + 0.2), 1)
		self.pos[1] += self.y_vel
