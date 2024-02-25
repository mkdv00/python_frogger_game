import pygame

from random import choice
from os import walk


class Car(pygame.sprite.Sprite):
    
    def __init__(self, pos, groups):
        super().__init__(groups)
        
        self.name = 'car'
        
        # image
        car_name = choice(list(walk('graphics/cars'))[0][2])
        self.image = pygame.image.load(file=f'graphics/cars/{car_name}').convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        
        # float based movement
        self.pos = pygame.math.Vector2(self.rect.center)
        
        if self.pos.x < 200:
            self.direction = pygame.math.Vector2(1, 0)
        else:
            self.direction = pygame.math.Vector2(-1, 0)
            self.image = pygame.transform.flip(surface=self.image, flip_x=True, flip_y=False)
            
        self.speed = 300
    
    def update(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        
        if not -200 < self.rect.x < 3400:
            self.kill()
        