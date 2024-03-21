import pygame

BASE_IMG_PATH = 'assets/'


def load_img(path, scale=2):
	img = pygame.image.load(BASE_IMG_PATH + path).convert()
	# TEMP: Scale image
	img = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
	img.set_colorkey((0, 0, 0))
	return img
