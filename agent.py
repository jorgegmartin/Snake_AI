import random
import numpy as np
import pandas as pd
import torch
from collections import deque
from game import SnakeGameAI, Direction, Point
from model import Linear_QNet, QTrainer
from helper import plot

MAX_MEMORY = 1_000_000 # definir memoria para guardar en deque
BATCH_SIZE = 10_000
LR = 0.001 # learning rate


class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.99 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft() si tenemos demasiados datos ira quitando los de la izquierda
        self.model = Linear_QNet(12, 24, 48, 128, 64, 3) # this is the number of neurons in our model, input, hidden, output
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma) #gamma is the discoutn rate, which needs to be less than 1


    def get_state(self, game):
        head = game.snake[0]
        point_l = Point(head.x - 20, head.y)
        point_r = Point(head.x + 20, head.y)
        point_u = Point(head.x, head.y - 20)
        point_d = Point(head.x, head.y + 20)

        point_2l = Point(head.x - 40, head.y)
        point_2r = Point(head.x + 40, head.y)
        point_2u = Point(head.x, head.y - 40)
        point_2d = Point(head.x, head.y + 40)
        
        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        state = [
            # Danger straight
            (dir_r and game.is_collision(point_r)) or 
            (dir_l and game.is_collision(point_l)) or 
            (dir_u and game.is_collision(point_u)) or 
            (dir_d and game.is_collision(point_d)),

            # Danger right
            (dir_u and game.is_collision(point_r)) or 
            (dir_d and game.is_collision(point_l)) or 
            (dir_l and game.is_collision(point_u)) or 
            (dir_r and game.is_collision(point_d)),

            # Danger left
            (dir_d and game.is_collision(point_r)) or 
            (dir_u and game.is_collision(point_l)) or 
            (dir_r and game.is_collision(point_u)) or 
            (dir_l and game.is_collision(point_d)),
            
            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # Food location 
            game.food.x < game.head.x,  # food left
            game.food.x > game.head.x,  # food right
            game.food.y < game.head.y,  # food up
            game.food.y > game.head.y,  # food down
            
            # Closed loop warning
            # Warning get into a loop
            (dir_r and game.is_collision(point_2r)) or 
            (dir_l and game.is_collision(point_2l)) or 
            (dir_u and game.is_collision(point_2u)) or 
            (dir_d and game.is_collision(point_2d))
            # and
            # 
            ]

        return np.array(state, dtype=int)


    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) #popleft if maxmemory is reached

    def train_long(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) #list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        #random moves: tradeoff exploration / exploitation
        self.epsilon = 200 - self.n_games # hardcoded so we can wiggle it
        final_move = [0, 0, 0]
        if random.randint(0, 200 < self.epsilon):
            move = random.randint(0, 2)
            final_move[move] = 1
        
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        
        return final_move
            

def train():
    plot_scores = []
    plot_mean_scores = []
    last_10 = list(np.zeros((20,), dtype=int))
    plot_10_mean = []
    total_score = 0
    mean_10_score = 0
    record = 0
    agent = Agent()
    game = SnakeGameAI()
    while True: # training loop
        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        #perform move and get nw state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory, plot results
            game.reset()
            agent.n_games +=1
            agent.train_long()

            if score > record:
                record = score
                agent.model.save()
            print('Game', agent.n_games, 'Score', 'Record: ', record)

            plot_scores.append(score)
            total_score += score

            last_10.append(score)
            mean_10_score = np.sum(last_10[-20:-1]) / 20
            plot_10_mean.append(mean_10_score)
                    
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores, plot_10_mean)

        





if __name__ =='__main__':
    train()


