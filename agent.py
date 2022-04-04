from matplotlib.pyplot import cla
import torch
import random
import numpy as np

from game import SnakeGameAI, Direction, Point

from collections import deque


MAX_MEMORY = 100_000
BATCH_SIZE = 1000
alpha = 0.001


class Agent:
    def __init__(self):
        self.number_games == 0
        self.epsilon = 0 #randomness
        self.gamma = 0 #discount rate
        self.memory = deque(maxlen=MAX_MEMORY) #popleft()





    def get_state(self, game):
        pass

    def remember(self, state, action, reward, next_state, done):
        pass

    def train_long_memory(self):
        pass

    def train_short_memory(self, state, action, reward, next_state, done):
        pass

    def get_action(self, state):
        pass


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGameAI()

    while True:
        #old state
        state_old = agent.get_state(game)

        #get move
        final_move = agent.get_action(state_old)

        #move and set new state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        #train on short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        #store memory

        agent.remember(state_old, final_move, reward, state_new, done)


        if done:
            #train on long memory, plot result
            game.reset()
            agent.number_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                #agent.model.save


if __name__ == '__main__':
    train()