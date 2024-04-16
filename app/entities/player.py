from . import *
from .entity import Entity


class Player(Entity):
	PLAYER_WIDTH = 32
	PLAYER_HEIGHT = 32
	PLAYER_SCALE = 2
	PLAYER_VEL = 4

	def __init__(self, x, y) -> None:
		super().__init__()
		rect_width = Player.PLAYER_WIDTH * Player.PLAYER_SCALE
		rect_height = Player.PLAYER_HEIGHT * Player.PLAYER_SCALE
		self.rect = pygame.Rect(
			x * rect_width,
			y * rect_height,
			rect_width,
			rect_height)
		self.mask = None
		self.vel = pygame.Vector2((0, 0))
		self.collide_left = False
		self.collide_right = False
		self.fall_count = 0
		self.jump_count = 0
		self.sheet = get_sprites_sheet(
			["main_characters", "ninja_frog"],
			Player.PLAYER_WIDTH,
			Player.PLAYER_HEIGHT,
			scale=Player.PLAYER_SCALE,
			direction=True)
		self.direction = "right"
		self.animation_count = 0
		self.head_sprite = pygame.sprite.Sprite()
		self.foot_sprite = pygame.sprite.Sprite()

	def loop(self, events: pygame.event, display: pygame.Surface, objs: list) -> None:
		self.update()
		self.move(events)
		self.collision(objs)
		self.gravity()
		self.draw(display)

	def update(self) -> None:
		self.update_sprites()
		self.update_rect()

	def update_sprites(self) -> None:
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
		max_animation_count = len(sprites) * ANIMATION_DELAY
		sprite_index = (self.animation_count % max_animation_count) // ANIMATION_DELAY
		self.sprite = sprites[sprite_index]
		self.animation_count = (self.animation_count + 1) % max_animation_count

	def update_rect(self) -> None:
		"""
		Update player's rect and mask.
		"""

		self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
		self.mask = pygame.mask.from_surface(self.sprite)
		self.head_rect = self.get_head_rect()
		self.foot_rect = self.get_foot_rect()

	def draw(self, display: pygame.Surface) -> None:
		# self.debug_hitbox(display)

		display.blit(self.sprite, (self.rect.x, self.rect.y))

	def debug_hitbox(self, display: pygame.Surface, offset=(0, 0)) -> None:
		"""
		Debug:
			Draw player's hitbox.
		"""

		pygame.draw.rect(display, (0, 255, 0), (
			self.rect.x - offset[0],
			self.rect.y - offset[1],
			self.rect.width,
			self.rect.height))
		pygame.draw.rect(display, (255, 0, 0), (
			self.head_rect.x - offset[0],
			self.head_rect.y - offset[1],
			self.head_rect.width,
			self.head_rect.height))
		pygame.draw.rect(display, (255, 0, 0), (
			self.foot_rect.x - offset[0],
			self.foot_rect.y - offset[1],
			self.foot_rect.width,
			self.foot_rect.height))

	def move(self, events: pygame.event) -> None:
		self.vel.x = 0
		keys = pygame.key.get_pressed()

		if keys[pygame.K_LEFT]:
			self.move_left()

		if keys[pygame.K_RIGHT]:
			self.move_right()

		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					self.jump()

		self.handle_move(self.vel.x, self.vel.y)

	def handle_move(self, dx, dy) -> None:
		"""
		Move player's rect by dx, dy.
		"""

		self.rect.x += dx
		self.rect.y += dy
		self.head_rect.x += dx
		self.head_rect.y += dy
		self.foot_rect.x += dx
		self.foot_rect.y += dy

	def move_left(self) -> None:
		if self.collide_left:
			return

		self.vel.x = -Player.PLAYER_VEL
		if self.direction != "left":
			self.direction = "left"

	def move_right(self) -> None:
		if self.collide_right:
			return

		self.vel.x = Player.PLAYER_VEL
		if self.direction != "right":
			self.direction = "right"

	def jump(self) -> None:
		if self.jump_count >= 2:
			return

		if self.jump_count == 0:
			self.vel.y = round(-Player.PLAYER_VEL * 1.5)
		elif self.jump_count == 1:
			self.vel.y = round(-Player.PLAYER_VEL * 3)

		self.animation_count = 0
		self.jump_count += 1
		if self.jump_count == 1:
			self.fall_count = 0

	def land(self) -> None:
		self.fall_count = 0
		self.vel.y = 0
		self.jump_count = 0

	def hit_head(self) -> None:
		self.vel.y = 0

	def collision(self, objs: list) -> None:
		self.vertical_collide(objs)

		dx_check = Player.PLAYER_VEL * 1.2
		self.collide_left = self.horizontal_collide(objs, -dx_check)
		self.collide_right = self.horizontal_collide(objs, dx_check)

	def vertical_collide(self, objs: list) -> None:
		self.head_sprite.rect = self.head_rect
		self.foot_sprite.rect = self.foot_rect

		for obj in objs:
			if pygame.sprite.collide_rect(self.head_sprite, obj):
				self.rect.top = obj.rect.bottom
				self.hit_head()

			if pygame.sprite.collide_rect(self.foot_sprite, obj):
				self.rect.bottom = obj.rect.top
				self.land()

	def horizontal_collide(self, objs: list, dx) -> bool:
		self.handle_move(dx, 0)

		collided = False
		for obj in objs:
			if pygame.sprite.collide_mask(self, obj):
				collided = True
				break

		self.handle_move(-dx, 0)
		return collided

	def get_head_rect(self) -> pygame.Rect:
		x_pos = 14
		y_pos = 8

		return pygame.Rect(
			self.rect.x + x_pos,
			self.rect.y + y_pos,
			self.rect.width - (x_pos * 2),
			2)

	def get_foot_rect(self) -> pygame.Rect:
		x_pos = 14
		y_pos = self.rect.height - 2

		return pygame.Rect(
			self.rect.x + x_pos,
			self.rect.y + y_pos,
			self.rect.width - (x_pos * 2),
			2)
