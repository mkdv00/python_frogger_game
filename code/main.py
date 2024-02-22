import sys
from random import choice, randint

import pygame
from car import Car
from player import Player
from settings import CAR_START_POSITIONS, WINDOW_HEIGHT, WINDOW_WIDTH


class AllSprites(pygame.sprite.Group):
    
    def __init__(self):
        super().__init__()
        self.offset = pygame.math.Vector2()
        self.bg = pygame.image.load(file='graphics/main/map.png').convert()
        self.fg = pygame.image.load(file='graphics/main/overlay.png').convert_alpha()
    
    def customize_draw(self):
        self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2
        
        # draw bg
        screen.blit(source=self.bg, dest=-self.offset)
        
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            screen.blit(source=sprite.image, dest=offset_pos)
        
        # fraw fg
        screen.blit(source=self.fg, dest=-self.offset)


# game setup
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Frogger')
clock = pygame.time.Clock()

# groups
all_sprites = AllSprites()

# sprites
player = Player(pos=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), groups=all_sprites)

# car timer
car_timer = pygame.event.custom_type()
pygame.time.set_timer(event=car_timer, millis=50)

# cars positions
car_pos_list = []

# game loop
while True:
    
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == car_timer:
            random_pos = choice(CAR_START_POSITIONS)
            pos = (random_pos[0], random_pos[1] + randint(-10, 10))
            
            if random_pos not in car_pos_list:
                car_pos_list.append(random_pos)
                Car(pos=pos, groups=all_sprites)
            
            if len(car_pos_list) > 5:
                del car_pos_list[0]
    
    # frame rate
    dt = clock.tick() / 1000
    
    # background
    screen.fill(color='black')
    
    # updates
    all_sprites.update(dt)
    
    # graphics
    all_sprites.customize_draw()
    
    # update the frame
    pygame.display.update()
    