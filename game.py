from pickletools import UP_TO_NEWLINE
from tkinter import LEFT, RIGHT
import pygame
import random


from enum import Enum

from zmq import DOWNSTREAM

pygame.init()

font = pygame.font.Font('arial.ttf', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

