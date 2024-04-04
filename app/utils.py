from . import *


def get_sprites(sub_dir: list, width, height, direction=False) -> dict:
	sprites = {}
	path = os.path.join(ASSETS_PATH, *sub_dir)

	for file in sorted(os.listdir(path)):
		if file.endswith(".png"):
			file_name = os.path.splitext(file)[0]
			sheets = pygame.image.load(os.path.join(path, file)).convert_alpha()

			raw_sprites = [pygame.transform.scale2x(
				sheets.subsurface(pygame.Rect(width * i, 0, width, height)))
				for i in range(sheets.get_width() // width)]
			print(raw_sprites)

			if direction:
				sprites[f"{file_name}_left"] = flip_sprites(raw_sprites)
				sprites[f"{file_name}_right"] = raw_sprites
			else:
				sprites[file_name] = raw_sprites

	return sprites


def flip_sprites(sprites: dict) -> dict:
	return [pygame.transform.flip(sprite, True, False) for sprite in sprites]
