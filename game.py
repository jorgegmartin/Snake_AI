import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init() # we need to initialize the game at the beggining

WIDTH = 720
HEIGHT = 480
BLOCK_SIZE = 20
SPEED = 100

font = pygame.font.Font('/home/dsc/Data_Science_Projects/Snake_AI/resources/fonts/font.TTF', 25)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
food_img = pygame.image.load('/home/dsc/Data_Science_Projects/Snake_AI/resources/imgs/snake_food.png').convert_alpha()


# reset
# reward
# play(action) -> direction
# game_iteration
# is collision





# Points is also prone to error so we will acces them through a tupple
Point = namedtuple('Point', 'x, y')

class Color:
    WHITE = (255, 255, 255)
    RED = (200, 0, 0)
    BLUE1 = (0, 0, 255)
    BLUE2 = (0, 100, 255)
    BLACK = (0, 0, 0)
    GREEN = (34, 177, 76)
    DARK_GREEN = (22, 114, 50)

class Direction(Enum): # since defining direction is prone to typing errors,
    UP = 1             # it is better to define a class from which we can acces directions
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class SnakeGameAI():

    def __init__(self, w=WIDTH, h=HEIGHT):
        self.w = w
        self.h = h
        # init display
        self.display = screen
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()

    def reset (self):
        # init game state
        self.direction = Direction.RIGHT
        self.head = Point(self.w/2, self.h/2)
        self.snake = [
                      self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)
                      ]

        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0 # we want to keep track of the game iteration
    
    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake: # we rerun the function if the food is placed inside the snake
            self._place_food()
    
    def play_step(self, action): # event handler definition
        self.frame_iteration += 1
        # 1. collect input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
     
        # 2 move the snake
        self._move(action) # update the head
        self.snake.insert(0, self.head) # we dont use append because we want it at the begining

        # 3 check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 50*len(self.snake): # game ends if collision or too much time without eating
            game_over = True
            reward = -100
            return reward, game_over, self.score

        # 4 place new food or move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()
            reward = 0.001 # reward survival    

        # 5 update the ui and clock
        self._update_ui()
        self.clock.tick(SPEED)


        # 6 return game over and score
        game_over = False
        return reward, game_over, self.score

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits body
        if pt in self.snake[1:]: #head is always within itself so we don't want to check the first position
            return True
        return False # if no collision is detected return false

    def _update_ui(self):
        self.display.fill(Color.BLACK) # we need to fill the screen first and then draw the snake
        self.image = food_img

        for point in self.snake:
            pygame.draw.rect(self.display, Color.DARK_GREEN, pygame.Rect(point.x, point.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, Color.GREEN, pygame.Rect(point.x+4, point.y+4, BLOCK_SIZE-8, BLOCK_SIZE-8))
        
        pygame.Surface.blit(self.display, self.image, (self.food.x, self.food.y))
        #pygame.draw.rect(self.display, Color.RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score  " + str(self.score), True, Color.WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip() # command to call for the changes

    def _move(self, action):
        # [straigh, right turn, left turn]

        clock_wise =[Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx] # no change in direction
        elif np.array_equal(action, [0, 1, 0]):
            new_dir = clock_wise[(idx + 1) % 4] # next index
        else:
            new_dir = clock_wise[(idx - 1) % 4]
        
        self.direction = new_dir

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

        self.head = Point(x, y) # update the head with the new values
