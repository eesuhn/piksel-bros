import pygame
import sys
import os
import psutil
import warnings
import json


FPS = 60
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 640
RECT_WIDTH = 64
RECT_HEIGHT = 64
CAM_SCALE = 1.6

PER_SEC_EVENT = pygame.USEREVENT + 1
