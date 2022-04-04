from pickletools import UP_TO_NEWLINE
from tkinter import LEFT, RIGHT
from wave import Wave_write
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



class SnakeGame:


    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h


        #display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()

        #game state

