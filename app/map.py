class Map:
	def __init__(self, game, tile_size=64):
		self.game = game
		self.tile_size = tile_size
		self.tiles = {}
		self.off_grid = []

		for i in range(10):
			# self.tiles[str(3 + i) + ';7'] = {'type': 'dirt', 'variant': 0, 'pos': (3 + i, 7)}
			# self.tiles[str(3 + i) + ';8'] = {'type': 'dirt', 'variant': 1, 'pos': (3 + i, 8)}
			self.tiles[(2 + i, 7)] = {'type': 'dirt', 'variant': 0}
			self.tiles[(2 + i, 8)] = {'type': 'dirt', 'variant': 1}

	def render(self, surf):
		for tile in self.off_grid:
			surf.blit(self.game.assets[tile['type']][tile['variant']], tile['pos'])

		# for loc in self.tiles:
		# 	tile = self.tiles[loc]
		# 	pos_x, pos_y = tile['pos']
		for pos, tile in self.tiles.items():
			pos_x, pos_y = pos
			surf.blit(
				self.game.assets[tile['type']][tile['variant']],
				(pos_x * self.tile_size, pos_y * self.tile_size))
