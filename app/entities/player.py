from . import *
from ..utils import get_sprites_sheet


class Player:
	def __init__(self, x, y) -> None:
		x *= PLAYER_WIDTH
		y *= PLAYER_HEIGHT
		self.rect = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
		self.mask = None
		self.x_vel = 0
		self.y_vel = 0
		self.fall_count = 0
		self.sheet = get_sprites_sheet(
			["main_characters", "ninja_frog"],
			PLAYER_WIDTH,
			PLAYER_HEIGHT,
			direction=True)
		self.direction = "right"
		self.animation_count = 0

	def loop(self, display: pygame.Surface, objs: list) -> None:
		self.update_sprites()
		self.move()
		self.collision(objs)
		self.gravity()
		self.draw(display)

	def update_sprites(self) -> None:
		sprites_sheet = "idle"

		if self.x_vel != 0:
			sprites_sheet = "run"

		sheet_name = f"{sprites_sheet}_{self.direction}"
		sprites = self.sheet[sheet_name]
		max_animation_count = len(sprites) * ANIMATION_DELAY
		sprite_index = (self.animation_count % max_animation_count) // ANIMATION_DELAY
		self.sprite = sprites[sprite_index]
		self.animation_count = (self.animation_count + 1) % max_animation_count
		self.update_mask()

	def update_mask(self) -> None:
		self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
		self.mask = pygame.mask.from_surface(self.sprite)

	def draw(self, display: pygame.Surface) -> None:
		display.blit(self.sprite, (self.rect.x, self.rect.y))

	def move(self) -> None:
		self.x_vel = 0
		keys = pygame.key.get_pressed()

		if keys[pygame.K_LEFT]:
			self.move_left()

		if keys[pygame.K_RIGHT]:
			self.move_right()

		self.handle_move(self.x_vel, self.y_vel)

	def handle_move(self, dx, dy) -> None:
		self.rect.x += dx
		self.rect.y += dy

	def move_left(self) -> None:
		self.x_vel = -PLAYER_VEL
		if self.direction != "left":
			self.direction = "left"

	def move_right(self) -> None:
		self.x_vel = PLAYER_VEL
		if self.direction != "right":
			self.direction = "right"

	def gravity(self) -> None:
		self.y_vel += min(1, self.fall_count / (PLAYER_VEL * 10))
		if self.fall_count < (PLAYER_VEL * 10):
			self.fall_count += 1

	def landed(self) -> None:
		self.fall_count = 0
		self.y_vel = 0

	def collision(self, objs: list) -> None:
		for obj in objs:
			if pygame.sprite.collide_mask(self, obj):
				if self.y_vel > 0:
					self.rect.bottom = obj.rect.top
					self.landed()
