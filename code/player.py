import pygame


class Player(pygame.sprite.Sprite):
    
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((50, 50))
        self.image.fill('red')
        self.rect = self.image.get_rect(center=pos)
    
    def input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            print('right')
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            print('left')
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            print('down')
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            print('up')
    
    def update(self):
        self.input()