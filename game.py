import pygame
import random

from enum import Enum
from tkinter import LEFT, RIGHT
from wave import Wave_write
from pickletools import UP_TO_NEWLINE
from collections import namedtuple


Point = namedtuple('Point', 'x, y')

pygame.init()

font = pygame.font.Font('arial.ttf', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4



BLOCK_SIZE = 20
SPEED = 20

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


        def play_step(self):

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            #user input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN

            
            #movement
            self._move(self.direction)
            self.snake.insert(0, self.head)

            #check game over
            game_over = False
            if self._is_collision():
                game_over = True
                return game_over, self.score



            #eat and place new food
            if self.head == self.food:
                self.score += 1
                self._place_food()
            else:
                self.snake.pop()

            
            #return game over and score
            self._update_ui()
            self.clock.tick(SPEED)

            return game_over, self.score
    

    def _is_collision(self):
        
        if self.head.x < 0 or self.head.x > self.w-BLOCK_SIZE or self.head.y < 0 or self.head.y > self.h-BLOCK_SIZE:
            return True
        elif self.head in self.snake:
            return True
        else:
            return False


            