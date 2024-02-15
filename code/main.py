import pygame, sys
from settings import WINDOW_WIDTH, WINDOW_HEIGHT

# game setup
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Frogger')
clock = pygame.time.Clock()

# game loop
while True:
    
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # frame rate
    dt = clock.tick() / 1000
    
    # draw the frame
    pygame.display.update()