class Physics:
	def __init__(self, game, e_type, pos, size):
		self.game = game
		self.e_type = e_type
		self.pos = list(pos)
		self.size = size
		self.velocity = [0, 0]

	def update(self, mov=(0, 0)):
		frame_mov = (mov[0] + self.velocity[0], mov[1] + self.velocity[1])

		self.pos[0] += frame_mov[0]
		self.pos[1] += frame_mov[1]

	def render(self, surf):
		surf.blit(self.game.assets['player'], self.pos)
