import pygame
import sys
import os
import psutil


from .utils import Utils
from .entities import *


FPS = 60
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 640
CPU_MONITOR_EVENT = pygame.USEREVENT + 1
