from pickletools import UP_TO_NEWLINE
from tkinter import LEFT, RIGHT
from wave import Wave_write
import pygame
import random
from collections import namedtuple



from enum import Enum

from zmq import DOWNSTREAM

Point = namedtuple('Point', 'x, y')

pygame.init()

font = pygame.font.Font('arial.ttf', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4



BLOCK_SIZE = 20

class SnakeGame:


    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h


        #display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()

        #game state

        self.direction = Direction.RIGHT

        self.head = Point(self.w/2 , self.h/2)

        self.snake = [
            self.head,
            Point(self.head.x-BLOCK_SIZE, self.head.y),
            Point(self.head.x-(2*BLOCK_SIZE), self.head.y)
        ]

        self.score = 0
        self.food = None
        self._place_food()

        def _place_food(self):
            #randomly placing food
            x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
            y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE

            self.food = Point(x, y)

            if self.food in self.snake:
                self._place_food()


        