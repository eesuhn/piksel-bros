class Map:
	def __init__(self, game, tile_size=64):
		self.game = game
		self.tile_size = tile_size
		self.map = {}
		self.off_grid = []

		for i in range(10):
			self.map[str(3 + i) + ';10'] = {'type': 'dirt', 'variant': 0, 'pos': (3 + i, 10)}
			self.map[str(3 + i) + ';11'] = {'type': 'dirt', 'variant': 1, 'pos': (3 + i, 11)}

	def render(self, surf):
		for tile in self.off_grid:
			surf.blit(self.game.assets[tile['type']][tile['variant']], tile['pos'])

		for loc in self.map:
			tile = self.map[loc]
			pos_x, pos_y = tile['pos']
			surf.blit(self.game.assets[tile['type']][tile['variant']], (pos_x * self.tile_size, pos_y * self.tile_size))
