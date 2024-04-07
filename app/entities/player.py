from . import *
from ..utils import get_sprites_sheet


class Player:
	def __init__(self, x, y) -> None:
		player_rect_width = PLAYER_WIDTH * PLAYER_SCALE
		player_rect_height = PLAYER_HEIGHT * PLAYER_SCALE
		self.rect = pygame.Rect(
			x * player_rect_width,
			y * player_rect_height,
			player_rect_width,
			player_rect_height
		)
		self.mask = None
		self.x_vel = 0
		self.y_vel = 0
		self.collide_left = False
		self.collide_right = False
		self.fall_count = 0
		self.jump_count = 0
		self.sheet = self.random_character()
		self.direction = "right"
		self.animation_count = 0
		self.head_sprite = pygame.sprite.Sprite()
		self.foot_sprite = pygame.sprite.Sprite()

	def random_character(self) -> dict:
		characters = os.listdir(os.path.join("assets", "main_characters"))
		character = random.choice(characters)

		return get_sprites_sheet(
			["main_characters", character],
			PLAYER_WIDTH,
			PLAYER_HEIGHT,
			scale=PLAYER_SCALE,
			direction=True)

	def loop(self, events: pygame.event, display: pygame.Surface, objs: list) -> None:
		self.update_sprites()
		self.update_rect()
		self.move(events)
		self.collision(objs)
		self.gravity()
		self.draw(display)

	def update_sprites(self) -> None:
		sprites_sheet = "idle"

		if self.y_vel < 0:
			if self.jump_count == 1:
				sprites_sheet = "jump"
			elif self.jump_count == 2:
				sprites_sheet = "double_jump"

		elif self.y_vel > 1:
			sprites_sheet = "fall"

		elif self.x_vel != 0:
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
		# Debug: Uncomment to see player's hitboxes
		# pygame.draw.rect(display, (255, 0, 0), self.head_rect)
		# pygame.draw.rect(display, (255, 0, 0), self.foot_rect)
		# pygame.draw.rect(display, (255, 0, 0), self.rect)

		display.blit(self.sprite, (self.rect.x, self.rect.y))

	def move(self, events: pygame.event) -> None:
		self.x_vel = 0
		keys = pygame.key.get_pressed()

		if keys[pygame.K_LEFT] and not self.collide_left:
			self.move_left()

		if keys[pygame.K_RIGHT] and not self.collide_right:
			self.move_right()

		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and self.jump_count < 2:
					self.jump()

		self.handle_move(self.x_vel, self.y_vel)

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
		self.x_vel = -PLAYER_VEL
		if self.direction != "left":
			self.direction = "left"

	def move_right(self) -> None:
		self.x_vel = PLAYER_VEL
		if self.direction != "right":
			self.direction = "right"

	def jump(self) -> None:
		if self.jump_count == 0:
			self.y_vel = round(-PLAYER_VEL * 1.5)
		elif self.jump_count == 1:
			self.y_vel = round(-PLAYER_VEL * 3)

		self.animation_count = 0
		self.jump_count += 1
		if self.jump_count == 1:
			self.fall_count = 0

	def gravity(self) -> None:
		self.y_vel += min(1, self.fall_count / (PLAYER_VEL * 10))
		if self.fall_count < (PLAYER_VEL * 10):
			self.fall_count += 1

	def land(self) -> None:
		self.fall_count = 0
		self.y_vel = 0
		self.jump_count = 0

	def hit_head(self) -> None:
		self.y_vel = 0

	def collision(self, objs: list) -> None:
		self.vertical_collide(objs)

		dx_check = PLAYER_VEL * 1.2
		self.collide_left = self.horizontal_collide(objs, -dx_check)
		self.collide_right = self.horizontal_collide(objs, dx_check)

	def vertical_collide(self, objs: list) -> None:
		self.head_sprite.rect = self.head_rect
		self.foot_sprite.rect = self.foot_rect

		for obj in objs:
			if pygame.sprite.collide_rect(self.head_sprite, obj) and self.y_vel < 0:
				self.rect.top = obj.rect.bottom
				self.hit_head()

			if pygame.sprite.collide_rect(self.foot_sprite, obj) and self.y_vel > 0:
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
		return pygame.Rect(
			self.rect.x + 14,
			self.rect.y + 8,
			self.rect.width - 28,
			2)

	def get_foot_rect(self) -> pygame.Rect:
		return pygame.Rect(
			self.rect.x + 14,
			self.rect.y + self.rect.height - 2,
			self.rect.width - 28,
			2)
