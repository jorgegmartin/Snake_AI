import pygame
import button # this is a file in the same folder
import os

#create display window
SCREEN_HEIGHT = 500
SCREEN_WIDTH = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Menu Screen')

#load button images
start_img = pygame.image.load('/home/dsc/Data_Science_Projects/Snake_AI/resources/imgs/start_btn.png').convert_alpha()
exit_img = pygame.image.load('/home/dsc/Data_Science_Projects/Snake_AI/resources/imgs/exit_btn.png').convert_alpha()

#create button instances
start_button = button.Button(100, 200, start_img, 0.8)
exit_button = button.Button(450, 200, exit_img, 0.8)

#game loop
run = True
while run:

	screen.fill((202, 228, 241))

	if start_button.draw(screen):
		os.system('/home/dsc/Data_Science_Projects/Snake_AI/Basic_Game/snake_game.py')
	if exit_button.draw(screen):
		pygame.quit()

	#event handler
	for event in pygame.event.get():
		#quit game
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()