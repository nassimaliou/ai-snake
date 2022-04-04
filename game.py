from tkinter.messagebox import NO
from chess import BLACK
import pygame
import random
import numpy as np

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
SPEED = 40

class SnakeGameAI:


    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h


        #display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
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
        self.frame_iteration = 0


    def _place_food(self):
        #randomly placing food
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE

        self.food = Point(x, y)

        if self.food in self.snake:
            self._place_food()


    def play_step(self, action):

        self.frame_iteration += 1
        reward = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            """
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
            """


        
        #movement
        self._move(action)
        self.snake.insert(0, self.head)

        #check game over
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score



        #eat and place new food
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()

        
        #return game over and score
        self._update_ui()
        self.clock.tick(SPEED)

        return reward, game_over, self.score


    def is_collision(self, pt=None):

        if pt is None:
            pt = self.head

        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True

        if pt in self.snake[1:]: #if it hits itself
            return True
        
        return False
    

    def _update_ui(self):
        self.display.fill((0, 0, 0))

        for pt in self.snake:
            pygame.draw.rect(self.display, (0, 125, 0) , (pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, (0, 255, 0) , (pt.x+4, pt.y+4, 12, 12))
        
        pygame.draw.rect(self.display, (200, 0, 0), pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        text = font.render("Score: "+ str(self.score), True, (255,255,255))
        self.display.blit(text, [0, 0])
        pygame.display.flip()
    



    def _move(self, action):

        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_direction = clock_wise[idx] #no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_direction = clock_wise[next_idx] #right turn
        else:
            next_idx = (idx - 1) % 4
            new_direction = clock_wise[next_idx] #left turn
        

        self.direction = new_direction


        x = self.head.x
        y = self.head.y

        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)





            