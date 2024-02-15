import pygame


class Player(pygame.sprite.Sprite):
    
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((50, 50))
        self.image.fill('red')
        self.rect = self.image.get_rect(center=pos)
        
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2()
        self.speed = 200
    
    def move(self, dt):
        if self.direction.magnitude():
            self.direction = self.direction.normalize()
        
        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))
    
    def input(self):
        keys = pygame.key.get_pressed()
        
        # horizontal movement
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0
        
        # vertical movement
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
        else:
            self.direction.y = 0
    
    def update(self, dt):
        self.input()
        self.move(dt)