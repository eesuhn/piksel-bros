from ._internal import *
from .entity import Entity
from ..utils import Utils


class Player(Entity):
	PLAYER_WIDTH = 32
	PLAYER_HEIGHT = 32
	PLAYER_VEL = 4
	ANIMATION_DELAY = 2.4

	def __init__(self, name, x, y, *groups) -> None:
		super().__init__(*groups)
		self.debug = "--debug" in sys.argv or "-d" in sys.argv

		self.rect = pygame.Rect(
			x * RECT_WIDTH,
			y * RECT_HEIGHT,
			RECT_WIDTH,
			RECT_HEIGHT)
		self.mask = None

		self.vel = pygame.Vector2((0, 0))
		self.collide_left = False
		self.collide_right = False
		self.fall_count = 0
		self.jump_count = 0

		self.sheet = Utils.get_sprites_sheet(
			["main_characters", name],
			self.PLAYER_WIDTH,
			self.PLAYER_HEIGHT,
			scale=(RECT_WIDTH // self.PLAYER_WIDTH),
			direction=True)
		self.image = pygame.Surface((RECT_WIDTH, RECT_HEIGHT)).convert_alpha()
		self.direction = "right"
		self.animation_count = 0
		self.static_image = Utils.get_image(
			["main_characters", name],
			"static")
		self.static_player = False

		self.head_rect, self.foot_rect = self._get_head_foot_rect()
		self.head_sprite = pygame.sprite.Sprite()
		self.foot_sprite = pygame.sprite.Sprite()

		if len(groups) > 0 and isinstance(groups[0], pygame.sprite.LayeredUpdates):
			groups[0].change_layer(self, 1)

	def update(self, **kwargs) -> None:
		"""
		Call in game loop
		"""
		for k, v in kwargs.items():
			setattr(self, k, v)

		if self.static_player:
			self._draw_static()
			return

		if self.debug:
			self._debug_hitbox()

		self._animate()
		self._move()
		self._collision()

	def _animate(self) -> None:
		sprites_sheet = "idle"

		if self.vel.y < 0:
			if self.jump_count == 1:
				sprites_sheet = "jump"
			elif self.jump_count == 2:
				sprites_sheet = "double_jump"

		elif self.vel.y > 1:
			sprites_sheet = "fall"

		elif self.vel.x != 0:
			sprites_sheet = "run"

		sheet_name = f"{sprites_sheet}_{self.direction}"
		sprites = self.sheet[sheet_name]
		max_animation_count = int(
			len(sprites) * self.ANIMATION_DELAY)
		sprite_index = int(
			(self.animation_count % max_animation_count) / self.ANIMATION_DELAY)
		self.animation_count = (self.animation_count + 1) % max_animation_count
		self.image = sprites[sprite_index]

		self.draw()

	def _draw_static(self) -> None:
		"""
		Draw static in editor
		"""
		pygame.draw.rect(
			self.image,
			(0, 255, 0),
			(0, 0, RECT_WIDTH, RECT_HEIGHT))
		self.image.blit(self.static_image, (0, 0))

		self.draw()

	def _update_rect_mask(self) -> None:
		"""
		Update `self.rect`, `self.mask`, `self.head_rect`, `self.foot_rect`
		"""
		self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
		self.mask = pygame.mask.from_surface(self.image)
		self.head_rect, self.foot_rect = self._get_head_foot_rect()

	def _debug_hitbox(self) -> None:
		"""
		Draw player's hitbox

		Args:
			`self.display`
		"""
		def draw_rect(rect, color) -> None:
			pygame.draw.rect(self.display, color, rect.move(
				-self.offset.x - self.top_left.x,
				-self.offset.y - self.top_left.y))

		draw_rect(self.rect, (0, 255, 0))
		draw_rect(self.head_rect, (255, 0, 0))
		draw_rect(self.foot_rect, (255, 0, 0))

	def _move(self) -> None:
		"""
		Capture input and move player

		Args:
			`self.events`
		"""
		self._update_rect_mask()

		self.vel.x = 0
		keys = pygame.key.get_pressed()

		if keys[pygame.K_LEFT]:
			self._move_left()

		if keys[pygame.K_RIGHT]:
			self._move_right()

		for event in self.events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					self._jump()

		self.handle_move(self.vel.x, self.vel.y)
		self._set_level_border()

	def _set_level_border(self) -> None:
		"""
		Keep player within level border
		"""
		if self.rect.x < self.top_left.x:
			self.rect.x = self.top_left.x
		if self.rect.right > self.bottom_right.x:
			self.rect.right = self.bottom_right.x

	def handle_move(self, dx, dy) -> None:
		"""
		Move player's rect by dx, dy
		"""
		self.rect.x += dx
		self.rect.y += dy
		self.head_rect.x += dx
		self.head_rect.y += dy
		self.foot_rect.x += dx
		self.foot_rect.y += dy

	def _move_left(self) -> None:
		if self.collide_left:
			return

		self.vel.x = -self.PLAYER_VEL
		if self.direction != "left":
			self.direction = "left"

	def _move_right(self) -> None:
		if self.collide_right:
			return

		self.vel.x = self.PLAYER_VEL
		if self.direction != "right":
			self.direction = "right"

	def _jump(self) -> None:
		if self.jump_count >= 2:
			return

		# Jump velocity based on jump count
		if self.jump_count == 0:
			self.vel.y = round(-self.PLAYER_VEL * 1.6)
		elif self.jump_count == 1:
			self.vel.y = round(-self.PLAYER_VEL * 1.8)

		self.fall_count = 0
		self.jump_count += 1
		self.animation_count = 0

	def _land(self) -> None:
		self.fall_count = 0
		self.jump_count = 0
		self.vel.y = 0

	def _hit_head(self) -> None:
		self.vel.y = 0

	def _collision(self) -> None:
		"""
		Args:
			`self.objs`
		"""
		self._vertical_collide(self.objs)

		dx_check = self.PLAYER_VEL * 1.2
		self.collide_left = self._horizontal_collide(self.objs, -dx_check)
		self.collide_right = self._horizontal_collide(self.objs, dx_check)

		self.gravity()

	def _vertical_collide(self, objs: list) -> None:
		self.head_sprite.rect = self.head_rect
		self.foot_sprite.rect = self.foot_rect

		for obj in objs:
			if pygame.sprite.collide_rect(self.head_sprite, obj):
				self.rect.top = obj.rect.bottom
				self._hit_head()
				break

			if pygame.sprite.collide_rect(self.foot_sprite, obj):
				self.rect.bottom = obj.rect.top
				self._land()
				break

	def _horizontal_collide(self, objs: list, dx) -> bool:
		self.handle_move(dx, 0)

		collided = False
		for obj in objs:
			if pygame.sprite.collide_mask(self, obj):
				collided = True
				break

		self.handle_move(-dx, 0)
		return collided

	def _get_head_foot_rect(self) -> tuple[pygame.Rect, pygame.Rect]:

		def _get_rect(x_pos, y_pos) -> pygame.Rect:
			return pygame.Rect(
				self.rect.x + x_pos,
				self.rect.y + y_pos,
				self.rect.width - (x_pos * 2),
				2)

		head_rect = _get_rect(14, 8)
		foot_rect = _get_rect(14, self.rect.height - 2)

		return head_rect, foot_rect
