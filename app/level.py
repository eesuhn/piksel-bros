from ._internal import *
from .entities import *
from .background import Background


class Level:
	def __init__(self) -> None:
		self.level = None
		self.objs = []

	def init_level(self, level: str) -> None:
		"""
		Load level data from json file
		"""
		self.level = level

		file = open(f"app/levels/{self.level}.json", "r")
		data = json.load(file)
		file.close()

		self.player = data["player"]
		self.background = data["background"]
		self.terrain = data["terrain"]

		self.obj_dict = {
			"terrain": self.terrain,
		}

	def load(self, camera: pygame.sprite.Group, target, edit=False) -> list:
		self.camera = camera
		camera.add_target(target)

		if not edit:
			Background(self.background, camera)

		self.load_objs()
		return self.objs

	def load_objs(self) -> None:
		self._load_terrain()

	def _load_terrain(self) -> None:
		for _, v in self.terrain.items():
			self.objs.append(
				Terrain(
					v["type"],
					v["var"],
					v["pos"][0],
					v["pos"][1],
					self.camera))

	def load_removed(self, x, y) -> None:
		if not self._remove_obj(x, y):
			return

		x *= RECT_WIDTH
		y *= RECT_HEIGHT

		for obj in self.objs:
			if obj.rect.x == x and obj.rect.y == y:
				obj.kill()

	def check_obj_list(self, x, y) -> str:
		"""
		Check if coordinates are in list of objects

		Returns:
			Object type if found, None otherwise
		"""
		key = f"{x};{y}"
		for obj_type, obj_list in self.obj_dict.items():
			if key in obj_list:
				return obj_type
		return None

	def _remove_obj(self, x, y) -> bool:
		obj_type = self.check_obj_list(x, y)
		if not obj_type:
			return False

		del self.obj_dict[obj_type][f"{x};{y}"]
		return True

	def get_min_max(self) -> tuple[pygame.Vector2, pygame.Vector2]:
		"""
		Get (top, left), (bottom, right) coordinates of the level
		"""
		min_x, min_y = float('inf'), float('inf')
		max_x, max_y = 0, 0

		for _, value in self.terrain.items():
			x, y = value["pos"]
			min_x = min(min_x, x)
			min_y = min(min_y, y)
			max_x = max(max_x, x)
			max_y = max(max_y, y)

		top_left = pygame.Vector2(
			min_x * RECT_WIDTH,
			min_y * RECT_HEIGHT)
		bottom_right = pygame.Vector2(
			(max_x + 1) * RECT_WIDTH,
			(max_y + 1) * RECT_HEIGHT)

		return top_left, bottom_right

	def get_size(self) -> tuple[int, int]:
		top_left, bottom_right = self.get_min_max()
		width = bottom_right.x - top_left.x
		height = bottom_right.y - top_left.y

		return width, height

	def save(self) -> None:
		file = open(f"app/levels/{self.level}.json", "w")
		json.dump(
			{
				"player": self.player,
				"background": self.background,
				"terrain": self.terrain,
			},
			file,
			indent="\t")
		file.close()

	def get_player_pos(self) -> pygame.Vector2:
		return pygame.Vector2((self.player["start"][0], self.player["start"][1]))

	def get_player_name(self) -> str:
		return self.player["name"]
