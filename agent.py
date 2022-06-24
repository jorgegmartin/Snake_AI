import torch
import random
import numpy as np
from collections import deque
from game import SnakeGameAI, Direction, Point

MAX_MEMORY = 100_000 # definir memoria para guardar en deque
BATCH_SIZE = 1000
LR = 0.001 # learning rate
torch 
class Agent:
    def __innit__(self):
        self.n_games = 0
        self.epsilon = 0 #randomness
        self.gamma = 0 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft() si tenemos demasiados datos ira quitando los de la izquierda
        self.model = None
        self.train = None
        # to do: model, trainer.


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
            game.food.y > game.head.y  # food down
            ]

        return np.array(state, dtype=int)


    def remember(self, state, action, reward, next_state, done):
        self.memory.append(state, action, reward, next_state, done) #popleft if maxmemory is reached

    def train_long(self):
        pass

    def train_short(self, state, action, reward, next_state, done):
        self.trainer

    def get_action(self, state):
        pass

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGameAI()
    while True: # training loop
        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_actions(state_old)

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
                # agent.model.save()
            print('Game', agent.n_games, 'Score', 'Record: ', record)

             #TODO: ploting

        





if __name__ =='__main__':
    train()


