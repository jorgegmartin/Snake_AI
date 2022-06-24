import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init() # we need to initialize the game at the beggining

font = pygame.font.Font('resources/fonts/font.ttf', 25)

WIDTH = 1280
HEIGHT = 720

class Direction(Enum): # since defining direction is prone to typing errors,
    UP = 1             # it is better to define a class from which we can acces directions
    DOWN = 2
    LEFT = 3
    RIGHT = 4

# Points is also prone to error
Point = namedtuple('Point', 'x, y')

class Color:
    WHITE = (255, 255, 255)
    RED = (200, 0, 0)
    BLUE1 = (0, 0, 255)
    BLUE2 = (0, 100, 255)
    BLACK = (0, 0, 0)

BLOCK_SIZE = 20
SPEED = 20

class SnakeGame():

    def __init__(self, w=WIDTH, h=HEIGHT):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()

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
    
    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake: # we rerun the function if the food is placed inside the snake
            self._place_food()
    
    def play_step(self): # event handler definition
        # 1. collect input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN: #user inputs
                if event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                    self.direction = Direction.LEFT 
                elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP and self.direction != Direction.DOWN:
                    self.direction = Direction.UP                                        
                elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                    self.direction = Direction.DOWN
     
        # 2 move the snake
        self._move(self.direction) # update the head
        self.snake.insert(0, self.head) # we dont use append because we eant it at the begining

        # 3 check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score

        # 4 place new food or move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()


        # 5 update the ui and clock
        self._update_ui()
        self.clock.tick(SPEED)


        # 6 return game over and score
        game_over = False
        return game_over, self.score

    def _is_collision(self):
        # hits boundary
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        # hits body
        if self.head in self.snake[1:]: #head is always within itself so we don't want to check the first position
            return True
        return False # if no collision is detected return false

    def _update_ui(self):
        self.display.fill(Color.BLACK) # we need to fill the screen first and then draw the snake

        for point in self.snake:
            pygame.draw.rect(self.display, Color.BLUE1, pygame.Rect(point.x, point.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, Color.BLUE2, pygame.Rect(point.x+4, point.y+4, BLOCK_SIZE-8, BLOCK_SIZE-8))
        
        pygame.draw.rect(self.display, Color.RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score  " + str(self.score), True, Color.WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip() # command to call for the changes

    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y) # update the head with the new values
        


if __name__ == '__main__':
    game = SnakeGame()
    # game loop

    while True:
        game_over, score = game.play_step()

        if game_over == True: # break the loop if game over is achieved.
            break

    print('Score', score)
    
    pygame.quit()
