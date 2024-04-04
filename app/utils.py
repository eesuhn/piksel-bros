from . import *


def get_sprites_sheet(sub_dir: list, width, height, direction=False) -> dict:
	sheet = {}
	path = os.path.join("assets", *sub_dir)

	for file in sorted(os.listdir(path)):
		if file.endswith(".png"):
			file_name = os.path.splitext(file)[0]
			sheets = pygame.image.load(os.path.join(path, file)).convert_alpha()

			raw_sprites = [pygame.transform.scale2x(
				sheets.subsurface(pygame.Rect(width * i, 0, width, height)))
				for i in range(sheets.get_width() // width)]

			if direction:
				sheet[f"{file_name}_left"] = flip_sprites(raw_sprites)
				sheet[f"{file_name}_right"] = raw_sprites
			else:
				sheet[file_name] = raw_sprites

	return sheet


def flip_sprites(sprites: list) -> list:
	return [pygame.transform.flip(sprite, True, False) for sprite in sprites]