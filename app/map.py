import pygame


class Map:
	NEIGHBOUR_OFFSETS = [
		(0, 0), (-1, 0), (-1, -1), (0, -1),
		(1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)
	]
	PHYSICS_TILES = {'dirt'}

	def __init__(self, game, tile_size=64):
		self.game = game
		self.tile_size = tile_size
		self.tiles = {}
		self.off_grid = []

		for i in range(10):
			self.tiles[str(i) + ';7'] = {'type': 'dirt', 'variant': 0, 'pos': (i, 7)}
			self.tiles[str(i) + ';8'] = {'type': 'dirt', 'variant': 1, 'pos': (i, 8)}

	def render(self, surf):
		for tile in self.off_grid:
			surf.blit(
				self.game.assets[tile['type']][tile['variant']],
				tile['pos'])

		for loc in self.tiles:
			tile = self.tiles[loc]
			pos_x, pos_y = tile['pos']
			surf.blit(
				self.game.assets[tile['type']][tile['variant']],
				(pos_x * self.tile_size, pos_y * self.tile_size))

	def tiles_around(self, pos):
		tiles = []
		tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
		for off_x, off_y in Map.NEIGHBOUR_OFFSETS:
			check_loc = str(tile_loc[0] + off_x) + ';' + str(tile_loc[1] + off_y)
			if check_loc in self.tiles:
				tiles.append(self.tiles[check_loc])
		return tiles

	def physics_rects_around(self, pos):
		rects = []
		for tile in self.tiles_around(pos):
			if tile['type'] in Map.PHYSICS_TILES:
				pos_x = tile['pos'][0] * self.tile_size
				pos_y = tile['pos'][1] * self.tile_size
				rects.append(pygame.Rect(pos_x, pos_y, self.tile_size, self.tile_size))
		return rects
