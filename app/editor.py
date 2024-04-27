from ._internal import *
from .entities import *
from .game import Game
from .camera import Camera


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
		self.obj_list = [
			os.listdir(os.path.join("assets", "terrain"))
		]
		self.terrain_type_c = 0
		self.terrain_type = self.obj_list[0][self.terrain_type_c]

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
			static_player=True)

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
		return f"{int(x)};{int(y)}" in self.level.terrain

	def add_block(self, x, y) -> None:
		if self.drag_player:
			return
		if self.is_block(x, y):
			return

		self.level.terrain[f"{x};{y}"] = {
			"type": self.terrain_type,
			"var": 1,
			"pos": [x, y]}
		self.level.load_added(x, y)

	def remove_block(self, x, y) -> None:
		if self.drag_player:
			return
		if not self.is_block(x, y):
			return

		del self.level.terrain[f"{x};{y}"]
		self.level.load_removed(x, y)

	def update_obj(self, event_btn: int) -> None:
		if event_btn == 4:
			self.terrain_type_c = (self.terrain_type_c + 1) % len(self.obj_list[0])
		if event_btn == 5:
			self.terrain_type_c = (self.terrain_type_c - 1) % len(self.obj_list[0])

		self.terrain_type = self.obj_list[0][self.terrain_type_c]
		print(f"{self.terrain_type_c}: {self.terrain_type}")


class EditorCamera(pygame.sprite.Sprite):
	CAM_VEL = 20

	def __init__(self, x, y, *groups) -> None:
		super().__init__(*groups)
		self.rect = pygame.Rect(x, y, SCREEN_WIDTH, SCREEN_HEIGHT)
		self.scroll = pygame.Vector2((x, y))

	def update(self, **kwargs) -> None:
		"""
		Call in game loop.
		"""

		self.move()

	def move(self) -> None:
		keys = pygame.key.get_pressed()
		dir_x = (keys[pygame.K_d] - keys[pygame.K_a]) * self.CAM_VEL
		dir_y = (keys[pygame.K_s] - keys[pygame.K_w]) * self.CAM_VEL

		if dir_x != 0 and dir_y != 0:
			dir_x *= 0.7071
			dir_y *= 0.7071

		self.rect.x += dir_x
		self.rect.y += dir_y
		self.scroll.x += dir_x
		self.scroll.y += dir_y
		self.set_border()

	def set_border(self) -> None:
		self.rect.x = max(0, self.rect.x)
		self.rect.y = max(0, self.rect.y)
		self.scroll.x = max(0, self.scroll.x)
		self.scroll.y = max(0, self.scroll.y)

	def mpos_to_wpos(self, o_screen: pygame.Vector2) -> pygame.Vector2:
		"""
		Returns world position based on mouse position.
		"""

		mpos = pygame.Vector2(pygame.mouse.get_pos())
		ratio_x = SCREEN_WIDTH * CAM_SCALE / o_screen.x
		ratio_y = SCREEN_HEIGHT * CAM_SCALE / o_screen.y
		adjust = pygame.Vector2((mpos.x * ratio_x, mpos.y * ratio_y))

		return pygame.Vector2((
			(adjust.x + self.scroll.x) // RECT_WIDTH,
			(adjust.y + self.scroll.y) // RECT_HEIGHT))
