import pygame, sys

from settings import WINDOW_WIDTH, WINDOW_HEIGHT
from player import Player
from car import Car

# game setup
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Frogger')
clock = pygame.time.Clock()

# groups
all_sprites = pygame.sprite.Group()

# sprites
player = Player(pos=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), groups=all_sprites)
car = Car(pos=(600, 200), groups=all_sprites)

# game loop
while True:
    
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # frame rate
    dt = clock.tick() / 1000
    
    # background
    screen.fill(color='black')
    
    # updates
    all_sprites.update(dt)
    
    # graphics
    all_sprites.draw(surface=screen)
    
    # update the frame
    pygame.display.update()
    