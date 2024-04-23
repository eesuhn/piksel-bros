from ._internal import *
from .entities import *
from .background import Background


class Level:
	def __init__(self) -> None:
		self.level = None
		self.map = {}
		self.on_grid = {}
		self.objs = []

	def load(self, level: str) -> None:
		self.level = level

		file = open(f"app/levels/{self.level}.json", "r")
		data = json.load(file)
		file.close()

		self.map = data
		self.player = data["player"]
		self.background = data["background"]
		self.on_grid = data["on_grid"]

	def init_level(self, camera: pygame.sprite.Group, target_player=True) -> list:
		self.camera = camera

		if target_player:
			Background(self.background, camera)
			camera.add_target(Player(
				self.player["start"][0],
				self.player["start"][1],
				camera))

		return self.render()

	def render(self) -> list:
		for key in self.on_grid:
			on = self.on_grid[key]
			self.objs.append(
				Terrain(
					on["type"],
					on["var"],
					on["pos"][0],
					on["pos"][1],
					self.camera))

		return self.objs

	def load_added(self, x, y) -> None:
		on = self.on_grid[f"{x};{y}"]
		self.objs.append(
			Terrain(
				on["type"],
				on["var"],
				on["pos"][0],
				on["pos"][1],
				self.camera))

	def load_removed(self, x, y) -> None:
		x *= RECT_WIDTH
		y *= RECT_HEIGHT

		for obj in self.objs:
			if obj.rect.x == x and obj.rect.y == y:
				obj.kill()

	def get_size(self, get_x_y=False) -> tuple:
		min_x, min_y = float('inf'), float('inf')
		max_x, max_y = float('-inf'), float('-inf')

		for _, value in self.on_grid.items():
			x, y = value["pos"]
			min_x = min(min_x, x)
			min_y = min(min_y, y)
			max_x = max(max_x, x)
			max_y = max(max_y, y)

		width = (max_x - min_x + 1) * RECT_WIDTH
		height = (max_y - min_y + 1) * RECT_HEIGHT

		if get_x_y:
			return width, height, min_x, min_y, max_x, max_y

		return width, height

	def save(self) -> None:
		file = open(f"app/levels/{self.level}.json", "w")
		json.dump(
			{
				"player": self.player,
				"background": self.background,
				"on_grid": self.on_grid,
			},
			file,
			indent="\t")
		file.close()
