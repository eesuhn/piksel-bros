import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
