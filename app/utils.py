import os
import pygame

BASE_IMG_PATH = 'assets/'


def load_img(path, scale=1):
	img = pygame.image.load(BASE_IMG_PATH + path).convert()
	img = pygame.transform.scale(
		img,
		(img.get_width() * scale, img.get_height() * scale))
	# img.set_colorkey((0, 0, 0))
	return img


def load_imgs(path, scale=1):
	imgs = []
	for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
		imgs.append(load_img(path + '/' + img_name, scale))
	return imgs
