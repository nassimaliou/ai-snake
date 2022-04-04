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
        self.model = None
        self.trainer = None





    def get_state(self, game):

        head = game.snake[0]

        point_l = Point(head.x - 20, head.y)
        point_r = Point(head.x + 20, head.y)
        point_u = Point(head.x, head.y - 20)
        point_d = Point(head.x, head.y + 20)
        
        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        state = [
            # Danger straight
            (dir_r and game.is_collision(point_r)) or (dir_l and game.is_collision(point_l)) or (dir_u and game.is_collision(point_u)) or (dir_d and game.is_collision(point_d)),

            # Danger right
            (dir_u and game.is_collision(point_r)) or (dir_d and game.is_collision(point_l)) or (dir_l and game.is_collision(point_u)) or (dir_r and game.is_collision(point_d)),

            # Danger left
            (dir_d and game.is_collision(point_r)) or (dir_u and game.is_collision(point_l)) or (dir_r and game.is_collision(point_u)) or (dir_l and game.is_collision(point_d)),
            
            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # Food location 
            game.food.x < game.head.x,  # food left
            game.food.x > game.head.x,  # food right
            game.food.y < game.head.y,  # food up
            game.food.y > game.head.y  # food down
            ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)


    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        #random move (tradeoff exploration / exploitation)

        self.epsilon = 80 - self.number_games

        final_move = [0, 0, 0]

        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model.predict(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
            
        return final_move


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

            print('Game', agent.number_games, 'Score', score, 'Record: ', record)




if __name__ == '__main__':
    train()