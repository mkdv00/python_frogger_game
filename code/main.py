import sys
from random import choice, randint

import pygame
from car import Car
from player import Player
from settings import *
from sprite import LongSprite, SimpleSprite


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
            pygame.draw.rect(surface=screen, color=(255, 255, 255), rect=sprite.hitbox, width=10)
        
        # fraw fg
        screen.blit(source=self.fg, dest=-self.offset)


# game setup
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Frogger')
clock = pygame.time.Clock()

# groups
all_sprites = AllSprites()
obstacles_group = pygame.sprite.Group()

# sprites
player = Player(pos=(2062, 3274), groups=all_sprites, collision_sprites=obstacles_group)

# car timer
car_timer = pygame.event.custom_type()
pygame.time.set_timer(event=car_timer, millis=50)

# cars positions
car_pos_list = []

# font
font = pygame.font.Font(None, size=50)
text_surf = font.render(text='You won!', antialias=True, color='White')
text_rect = text_surf.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

# music
bg_music = pygame.mixer.Sound(file='audio/music.mp3')
bg_music.play(loops= -1)

# sprite setup
# simple objects
for file_name, pos_list in SIMPLE_OBJECTS.items():
    path = f'graphics/objects/simple/{file_name}.png'
    surf = pygame.image.load(file=path).convert_alpha()
    
    for pos in pos_list:
        SimpleSprite(surf=surf, pos=pos, groups=[all_sprites, obstacles_group])

# long objects
for file_name, pos_list in LONG_OBJECTS.items():
    path = f'graphics/objects/long/{file_name}.png'
    surf = pygame.image.load(file=path).convert_alpha()
    
    for pos in pos_list:
        LongSprite(surf=surf, pos=pos, groups=[all_sprites, obstacles_group])

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
                Car(pos=pos, groups=[all_sprites, obstacles_group])
            
            if len(car_pos_list) > 5:
                del car_pos_list[0]
    
    # frame rate
    dt = clock.tick() / 1000
    
    # background
    screen.fill(color='black')
    
    if player.pos.y >= 1180:
        # updatesa
        all_sprites.update(dt)
        
        # graphics
        all_sprites.customize_draw()
    else:
        screen.fill(color='teal')
        screen.blit(source=text_surf, dest=text_rect)
        pygame.draw.rect(surface=screen, color='White', rect=text_rect.inflate(30, 30), width=8, border_radius=5)
    
    # update the frame
    pygame.display.update()
    