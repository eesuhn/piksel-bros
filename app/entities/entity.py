import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self, *groups: pygame.sprite.Group):
        super().__init__(*groups)
