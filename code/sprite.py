import pygame
from pygame import Rect, Surface


class SimpleSprite(pygame.sprite.Sprite):
    
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        
        self.image: Surface = surf
        self.rect: Rect = self.image.get_rect(topleft=pos)
        self.hitbox: Rect = self.rect.inflate(0, -self.rect.height / 2)


class LongSprite(pygame.sprite.Sprite):
    
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        
        self.image: Surface = surf
        self.rect: Rect = self.image.get_rect(topleft=pos)
        self.hitbox: Rect = self.rect.inflate(-self.rect.width * 0.8, -self.rect.height / 2)
        self.hitbox.bottom = self.rect.bottom - 10
