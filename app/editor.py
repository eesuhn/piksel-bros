from ._internal import *
from .entities import *
from .game import Game
from .camera import Camera
from .editor_camera import EditorCamera
from .utils import *


class Editor(Game):
	def __init__(self) -> None:
		super().__init__()
		pygame.display.set_caption("Editor - Piksel Bros.")
		self.display = pygame.Surface((
			SCREEN_WIDTH * CAM_SCALE,
			SCREEN_HEIGHT * CAM_SCALE)).convert_alpha()

		self.left_click = False
		self.right_click = False

		self.wpos = pygame.Vector2((0, 0))
		self.o_screen = pygame.Vector2((self.screen.get_size()))

		self.init_obj_list()

	def init_obj_list(self) -> None:
		self.obj_list = {
			"terrain": os.listdir(os.path.join("assets", "terrain")),
		}
		self.cats = list(self.obj_list.keys())
		self.current_cat_i = 0
		self.current_obj_i = 0
		self.update_current_obj()

	def load_level(self) -> None:
		self.level.init_level("01")

		self.camera = Camera()
		player_name = self.level.get_player_name()
		self.player_pos = self.level.get_player_pos()
		self.player = Player(player_name, self.player_pos.x, self.player_pos.y, self.camera)

		cam_pos = pygame.Vector2((
			(self.player_pos.x * RECT_WIDTH) - (SCREEN_WIDTH // 2),
			(self.player_pos.y * RECT_HEIGHT) - (SCREEN_HEIGHT // 2)
		))
		self.editor_camera = EditorCamera(cam_pos.x, cam_pos.y, self.camera)

		self.drag_player = False
		self.player_opos = self.player_pos
		self.player_dpos = self.player_pos

		self.level.load(self.camera, self.editor_camera, edit=True)

	def loop(self) -> None:
		self.display.fill((0, 0, 0))

		self.check_mouse()
		self.camera.update(
			display=self.display,
			top_left=pygame.Vector2((0, 0)),
			static_player=True,
			current_obj=self.get_current_obj())

		self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
		pygame.display.update()

	def check_event(self) -> None:
		super().check_event()

		for event in self.events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				self.handle_mousebuttondown(event)
			if event.type == pygame.MOUSEBUTTONUP:
				self.handle_mousebuttonup(event)
			if event.type == pygame.VIDEORESIZE:
				self.o_screen = pygame.Vector2((event.w, event.h))

	def handle_keydown(self, event: pygame.event.Event) -> None:
		super().handle_keydown(event)

		if event.key == pygame.K_RETURN:
			self.level.save()

	def handle_mousebuttondown(self, event: pygame.event.Event) -> None:
		if event.button == 1:
			if not self.right_click:
				self.left_click = True
		if event.button == 3:
			if not self.left_click:
				self.right_click = True
		if event.button == 4 or event.button == 5:
			self.update_obj(event.button)

	def handle_mousebuttonup(self, event: pygame.event.Event) -> None:
		if event.button == 1:
			self.left_click = False
		if event.button == 3:
			self.right_click = False

	def check_mouse(self) -> None:
		self.wpos = self.editor_camera.mpos_to_wpos(self.o_screen)
		x, y = int(self.wpos.x), int(self.wpos.y)

		if self.left_click:
			if not self.mpos_is_player_pos():
				self.add_block(x, y)
			else:
				self.drag_start()
		else:
			self.drag_end()

		if self.right_click:
			self.remove_block(x, y)

	def mpos_is_player_pos(self) -> bool:
		return self.wpos.x == self.player_pos.x and self.wpos.y == self.player_pos.y

	def drag_start(self) -> None:
		if self.drag_player:
			return
		self.drag_player = True

	def drag_end(self) -> None:
		if not self.drag_player:
			return
		self.drag_player = False

		if self.is_block(self.wpos.x, self.wpos.y):
			return
		self.move_player()

	def move_player(self) -> None:
		self.player_dpos = self.wpos

		x = (self.player_dpos.x - self.player_opos.x) * self.player.rect.width
		y = (self.player_dpos.y - self.player_opos.y) * self.player.rect.height
		self.player.handle_move(int(x), int(y))

		self.level.player["start"] = [
			int(self.player_dpos.x),
			int(self.player_dpos.y)]

		self.player_opos = self.wpos
		self.player_pos = self.wpos

	def is_block(self, x, y) -> bool:
		return self.level.check_obj_list(x, y) is not None

	def add_block(self, x, y) -> None:
		"""
		Check current category before adding block
		"""
		if self.drag_player:
			return
		if self.is_block(x, y):
			return

		if self.current_cat == "terrain":
			self.level.terrain[f"{x};{y}"] = {
				"type": self.current_obj,
				"var": 1,
				"pos": [x, y]}

		self.level.load_objs()

	def remove_block(self, x, y) -> None:
		if self.drag_player:
			return
		if not self.is_block(x, y):
			return

		self.level.load_removed(x, y)

	def update_current_obj(self) -> None:
		self.current_cat = self.cats[self.current_cat_i]
		self.current_obj = self.obj_list[self.current_cat][self.current_obj_i]

	def update_obj(self, event_btn: int) -> None:
		"""
		Update current object or category
		"""
		left_shift = pygame.key.get_pressed()[pygame.K_LSHIFT]

		if left_shift:
			if event_btn == 4:
				self.current_cat_i = (self.current_cat_i + 1) % len(self.cats)
			if event_btn == 5:
				self.current_cat_i = (self.current_cat_i - 1) % len(self.cats)
			self.current_obj_i = 0
		else:
			self.current_cat = self.cats[self.current_cat_i]
			if event_btn == 4:
				self.current_obj_i = (self.current_obj_i + 1) % len(self.obj_list[self.current_cat])
			if event_btn == 5:
				self.current_obj_i = (self.current_obj_i - 1) % len(self.obj_list[self.current_cat])

		self.update_current_obj()

	def get_current_obj(self) -> pygame.Surface:
		current_obj = get_image([self.current_cat, self.current_obj], "1")
		current_obj.set_alpha(150)
		return current_obj
