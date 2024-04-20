from ._internal import *
from .entities import *
from .background import Background


class Level:
	def __init__(self) -> None:
		self.map = {}
		self.on_grid = {}
		self.objs = []

	def load(self, level: str) -> None:
		file = open(f"app/levels/{level}.json", "r")
		data = json.load(file)
		file.close()

		self.map = data
		self.player = data["player"]
		self.background = data["background"]
		self.on_grid = data["on_grid"]

	def init_level(self, level: str, camera: pygame.sprite.Group, target_player=True) -> list:
		self.load(level)

		if target_player:
			Background(self.background, camera)
			camera.add_target(Player(
				self.player["start"][0],
				self.player["start"][1],
				camera))

		for key in self.on_grid:
			on = self.on_grid[key]
			self.objs.append(
				Terrain(
					on["type"],
					on["var"],
					on["pos"][0],
					on["pos"][1],
					camera))

		return self.objs

	def get_size(self, level: str) -> tuple:
		self.load(level)

		min_x, min_y = float('inf'), float('inf')
		max_x, max_y = 0, 0

		for key, value in self.map["on_grid"].items():
			x, y = value["pos"]
			min_x = min(min_x, x)
			min_y = min(min_y, y)
			max_x = max(max_x, x)
			max_y = max(max_y, y)

		width = (max_x - min_x + 1) * RECT_WIDTH
		height = (max_y - min_y + 1) * RECT_HEIGHT

		return width, height

	def save(self, level: str) -> None:
		file = open(f"app/levels/{level}.json", "w")
		json.dump(
			{
				"on_grid": self.on_grid,
			},
			file)
		file.close()
