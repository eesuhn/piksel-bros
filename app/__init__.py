import pygame
import sys
import os
import random
import psutil


FPS = 60
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 640
ANIMATION_DELAY = 3
DEFAULT_OFFSET = [0, 32]
OFFSET_DELAY = 4
CPU_MONITOR_EVENT = pygame.USEREVENT + 1
